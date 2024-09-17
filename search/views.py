from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.response import TemplateResponse
from wagtail.models import Page
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q, Value
from documentation.models import DocumentationPage

from wagtail.contrib.search_promotions.models import Query  # Ensure this is imported


def search(request):
    search_query = request.GET.get("query", None)
    page = request.GET.get("page", 1)

    if search_query:
        # Perform TrigramDistance search on both the title and hPeading_texts
        search_results = DocumentationPage.objects.live().annotate(
            title_similarity=TrigramSimilarity('title', Value(search_query)),
            heading_similarity=TrigramSimilarity('heading_texts', Value(search_query)),
        ).filter(
            Q(title_similarity__gte=0.3) | Q(heading_similarity__gte=0.3)
        ).order_by('-title_similarity', '-heading_similarity')

        # Log the search query
        query = Query.get(search_query)
        query.add_hit()

    else:
        search_results = DocumentationPage.objects.none()

    # Pagination (unchanged)
    paginator = Paginator(search_results, 10)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    return TemplateResponse(
        request,
        "search/search.html",
        {
            "search_query": search_query,
            "search_results": search_results,
        },
    )

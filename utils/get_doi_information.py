from crossref.restful import Works


def format_harvard(data):
    """Gets reference information from cross-ref api response and creates citation"""
    authors = data.get("author", [])

    date_parts = data.get("published-print", {}).get("date-parts", [])
    year = date_parts[0][0] if date_parts and date_parts[0] else ""

    title = data.get("title", [""])[0]
    journal = data.get("short-container-title", [""])[0]
    volume = data.get("volume", "")
    issue = data.get("issue", "")
    pages = data.get("page", "")
    publisher = data.get("publisher", "")
    doi = data.get("DOI", "")

    author_list = ", ".join(
        [f"{author['family']}, {author['given'][0]}." for author in authors]
    )

    citation = f'{author_list} ({year}) "{title}." *{journal}*, {volume}({issue}), {pages}. {publisher}. doi:{doi}'
    return {
        "title": title,
        "year": year,
        "journal": journal,
        "volume": volume,
        "citation": citation,
        "doi": doi,
    }


def doi_crossref_search(doi: str):
    works = Works()
    try:
        search = works.doi(doi)
    except TypeError:
        return None
    else:
        reference_dict = format_harvard(search)
        return reference_dict

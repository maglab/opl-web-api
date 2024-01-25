from xml.etree import ElementTree as ET

import requests


class PMIDRequestException(Exception):
    def __init__(self, message):
        super().__init__(message)


def get_pmid_citation(pmid):
    """Get the full text citation for a given pubmed id using NCBI API."""
    endpoint = "https://api.ncbi.nlm.nih.gov/lit/ctxp/v1/pubmed/"
    params = {"format": "citation", "id": pmid}
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return PMIDRequestException("An error occurred during the request:" + str(e))
    else:
        response_json = response.json()
        apa_citation = response_json["apa"]["format"]
        return apa_citation


def extract_text(element, xpath):
    result = element.find(xpath)
    return result.text if result is not None else None


def get_pmid_information(pmid):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    endpoint = "efetch.fcgi"
    db = "pubmed"
    retmode = "xml"

    url = f"{base_url}{endpoint}?db={db}&id={pmid}&retmode={retmode}"
    response = requests.get(url)

    if response.status_code == 200:
        root = ET.fromstring(response.text)
        author_list = root.find(".//AuthorList")

        primary_author_last_name = extract_text(author_list[0], ".//LastName")
        primary_author_initial = extract_text(author_list[0], ".//Initials")

        author = (
            f"{primary_author_last_name}, {primary_author_initial}"
            if primary_author_last_name and primary_author_initial
            else None
        )
        title = extract_text(root, ".//ArticleTitle")
        year = extract_text(root, ".//PubDate/Year")
        journal = extract_text(root, ".//Title")
        volume = extract_text(root, ".//Volume")

        doi_elem = root.find(".//ArticleId[@IdType='doi']")
        doi = doi_elem.text if doi_elem is not None else None

        return {
            "title": title,
            "author": author,
            "year": year,
            "journal": journal,
            "volume": volume,
            "doi": doi,
        }
    else:
        raise ValueError("Failed API Call to Entrez")


if __name__ == "__main__":
    get_pmid_information(36599349)

import requests
from xml.etree import ElementTree as ET


class PMIDRequestException(Exception):
    def __init__(self, message):
        super().__init__(message)


def get_pmid_citation(pmid):
    """Get the full text citation for a given pubmed id using NCBI API."""
    endpoint = "https://api.ncbi.nlm.nih.gov/lit/ctxp/v1/pubmed/"
    params = {
        "format": "citation",
        "id": pmid
    }
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return PMIDRequestException("An error occurred during the request:" + str(e))
    else:
        response_json = response.json()
        apa_citation = response_json["apa"]["format"]
        return apa_citation


def get_pmid_information(pmid):
    "Extracts specific information from a given PMID: Title, journal, authors, volume, year"
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    endpoint = "efetch.fcgi"
    db = "pubmed"
    retmode = "xml"

    url = f"{base_url}{endpoint}?db={db}&id={pmid}&retmode={retmode}"
    response = requests.get(url)

    if response.status_code == 200:
        root = ET.fromstring(response.text)

        title = root.find(".//ArticleTitle").text
        year = root.find(".//PubDate/Year").text
        journal = root.find(".//Title").text
        try:
            volume = root.find(".//Volume").text
        except AttributeError:
            volume = None
        doi_elem = root.find(".//ArticleId[@IdType='doi']")
        doi = doi_elem.text if doi_elem is not None else None

        return {"title": title, "year": year, "journal": journal, "volume": volume, "doi": doi}
    else:
        return ValueError("Failed API Call to Entrez")


if __name__ == "__main__":
    get_pmid_citation("1231231")
    pmid_info = get_pmid_information("1231231")

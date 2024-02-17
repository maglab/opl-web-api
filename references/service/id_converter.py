from xml.etree import ElementTree as ET

import requests
from crossref.restful import Works


class PMIDRequestException(Exception):
    def __init__(self, message):
        super().__init__(message)


class Converter:

    """
    Base class for converting
    """

    __response_data = None
    reference_dictionary = {}

    def __init__(self, identifier, journal_model, author_model):
        self.identifier = identifier
        self.Journal = journal_model
        self.Author = author_model

    def _create_journal_instance(self):
        """
        Format reference_dict reference instance using dictionary of reference information. Needed only because journal is a foreign key
        and submitted journal data is a string.
        """
        journal_instance, created = self.Journal.objects.get_or_create(
            journal_name=self.reference_dictionary["journal"]
        )
        self.reference_dictionary["journal_id"] = journal_instance

    def _create_author_instance(self):
        """
        Convert list of authors into author instances and inset back into reference_dictionary
        """
        author_instances = []
        for author in self.reference_dictionary["authors"]:
            author_instance, created = self.Author.objects.get_or_create(
                author_name=author
            )
            author_instances.append(author_instance)
        self.reference_dictionary["authors"] = author_instances


class DoiConverter(Converter):
    crossref_works = Works

    def __init__(self, identifier, journal, author):
        super().__init__(identifier, journal, author)

    def __format_reference(self):
        """Gets reference information from cross-ref api response and creates citation"""
        authors = self.__response_data.get("author", [])
        date_parts = self.__response_data.get("published-print", {}).get(
            "date-parts", []
        )
        year = date_parts[0][0] if date_parts and date_parts[0] else ""
        title = self.__response_data.get("title", [""])[0]
        journal = self.__response_data.get("short-container-title", [""])[0]
        volume = self.__response_data.get("volume", "")
        issue = self.__response_data.get("issue", "")
        pages = self.__response_data.get("page", "")
        publisher = self.__response_data.get("publisher", "")
        doi = self.__response_data.get("DOI", "")

        author_list = ", ".join(
            [f"{author['family']}, {author['given'][0]}." for author in authors]
        )

        citation = f'{author_list} ({year}) "{title}." *{journal}*, {volume}({issue}), {pages}. {publisher}. doi:{doi}'
        self.reference_dictionary = {
            "title": title,
            "authors": author_list,
            "year": year,
            "journal": journal,
            "volume": volume,
            "citation": citation,
            "doi": doi,
        }

    def __send_request(self):
        works = self.crossref_works()
        try:
            search = works.doi(self.identifier)
        except TypeError:
            raise TypeError("Unable to find DOI from crossref API")
        else:
            self.__response_data = search

    def retrieve_reference(self):
        # Retrieve reference information and populate reference dictionary
        self.__send_request()
        self.__format_reference()
        # Create instances
        self._create_journal_instance()
        self._create_journal_instance()
        return self.reference_dictionary


class PmidConverter(Converter):
    # Attributes for entrez api request
    __base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    __end_point = "efetch.fcgi"
    __database = "pubmed"
    __retmode = "xml"

    # Attributes for NCBI API citation request
    __base_url_ncbi = "https://api.ncbi.nlm.nih.gov/lit/ctxp/v1/pubmed/"

    def __init__(self, identifier, journal, author):
        super().__init__(identifier, journal, author)

    def __send_request(self):
        url = f"{self.__base_url}{self.__end_point}?db={self.__database}&id={self.identifier}&retmode={self.__retmode}"
        response = requests.get(url)
        if response.status_code == 200:
            self.__response_data = response.text
        else:
            raise ValueError("Failed api call to Entrez")

    def get_pmid_citation(self):
        """Get the full text citation for a given pubmed id using NCBI API."""
        endpoint = "https://api.ncbi.nlm.nih.gov/lit/ctxp/v1/pubmed/"
        params = {"format": "citation", "id": self.identifier}
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return PMIDRequestException(
                "An error occurred during the request:" + str(e)
            )
        else:
            response_json = response.json()
            apa_citation = response_json["apa"]["format"]
            return apa_citation

    @staticmethod
    def __extract_text(element, xpath):
        """
        Helper function to extract text from element using its xpath
        Args:
            element - XML element
            xpath - Xpath of elements withinn element
        Returns:
            results - String | None depending on if element is found
        """
        result = element.find(xpath)
        return result.text if result is not None else None

    def __extract_authors(self, author_list):
        """
        Extract author names from list of authors XML tag. Last name first and initials last.
        Args:
            author_list: list - XML Tag representing list of authors
        Returns:
            authors: list - List containing names of authors as strings
        """
        authors = []
        for author in author_list.findall(".//Author"):
            last_name = self.__extract_text(author, ".//LastName")
            initials = self.__extract_text(author, ".//Initials")
            if last_name and initials:
                authors.append(f"{last_name}, {initials}")
        return authors

    def __format_reference(self):
        root = ET.fromstring(self.__response_data)
        author_list = root.find(".//AuthorList")
        authors = self.__extract_authors(author_list)
        title = self.__extract_text(root, ".//ArticleTitle")
        year = self.__extract_text(root, ".//PubDate/Year")
        journal = self.__extract_text(root, ".//Title")
        volume = self.__extract_text(root, ".//Volume")
        doi_elem = root.find(".//ArticleId[@IdType='doi']")
        doi = doi_elem.text if doi_elem is not None else None

        self.reference_dictionary = {
            "title": title,
            "authors": authors,
            "year": year,
            "journal": journal,
            "volume": volume,
            "citation": self.get_pmid_citation(),
            "doi": doi,
        }

    def retrieve_reference(self):
        # Create the reference dictionary
        self.__send_request()
        self.get_pmid_citation()
        self.__format_reference()

        # Reformat the reference dictionary and insert model instances

        super()._create_author_instance()
        super()._create_journal_instance()
        return self.reference_dictionary

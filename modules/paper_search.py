import re

from scholarly import scholarly

from modules.model import Paper


class PaperSearch:
    def execute(self, keyword, limit) -> list[Paper]:
        raise NotImplementedError


class GoogleScholerSearch(PaperSearch):
    def execute(self, keyword, limit) -> list[Paper]:
        search_results = scholarly.search_pubs(keyword, sort_by="date")

        sliced_results = []
        for _ in range(limit):
            try:
                sliced_results.append(self.convert(next(search_results)))
            except StopIteration:
                break

        return sliced_results

    def convert(self, search_result) -> Paper:
        abstract = search_result["bib"]["abstract"]
        submitted_at = re.search(r"\d+ days ago - ", abstract)

        if submitted_at:
            abstract = abstract[len(submitted_at.group()) :]
            submitted_at = submitted_at.group().replace(" - ", "")

        return Paper(
            title=search_result["bib"]["title"],
            abstract=abstract,
            authors=search_result["bib"]["author"],
            url=search_result.get("pub_url"),
            submitted_at=submitted_at,
        )

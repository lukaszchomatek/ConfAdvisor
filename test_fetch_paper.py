from fetch_paper import fetch_paper

if __name__ == "__main__":
    url = "https://conf.researchr.org/details/fse-2025/fse-2025-industry-papers/39/Quantifying-the-benefits-of-code-hints-for-refactoring-deprecated-Java-APIs"
    path = fetch_paper(url)
    print(f"Zapisano dane w pliku: {path}")

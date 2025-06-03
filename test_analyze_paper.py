from analyze_paper import analyze_paper
import glob

if __name__ == "__main__":
    for path in glob.glob("papers/*.json"):
        try:
            analyze_paper(path)
            print(f"Zaktualizowano plik: {path}")
        except Exception as e:
            print(f"Błąd dla {path}: {e}")

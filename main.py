from pathlib import Path

from utils.oos_analyzer import compare_oos
from utils.web_scrape import scrape_character
from character.characters import CHARACTERS

output_dir = Path("data/raw")

def download_all_characters(CHARACTERS):
    for character in CHARACTERS:
        try:
            df = scrape_character(character.slug)

            print(f"Scraped {len(df)} moves for {character.name}")
            print("\nPreview:")
            print(df[['section', 'move', 'startup', 'active_frames', 'damage', 'advantage_on_shield']].head(15))
            
            # Save
            file_path = output_dir / f"{character.slug}_moves.csv"
            df.to_csv(file_path, index=False)
            print(f"\nSaved to {file_path}")
        except Exception as e:
                print(f"Error scraping {character.name}: {e}")

def main():
    #download_all_characters(CHARACTERS)
    compare_oos("Mario", "Luigi")
    
    print("\nScript Complete...")

if __name__ == '__main__':
    main()
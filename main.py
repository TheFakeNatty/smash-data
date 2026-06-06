from pathlib import Path

from utils.web_scrape import scrape_character
from character.characters import CHARACTERS

output_dir = Path("data/raw")
def main():
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
    
    print("\nScript Complete...")

if __name__ == '__main__':
    main()
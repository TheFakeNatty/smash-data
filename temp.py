import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def scrape_character(character_slug="mario"):
    url = f"https://ultimateframedata.com/{character_slug}"
    headers = {"User-Agent": "Mozilla/5.0 (compatible; DataScienceProject/1.0)"}
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    
    moves = []
    current_section = None
    
    # Find all section headers
    for h2 in soup.find_all('h2', class_='movecategory'):
        current_section = h2.get_text(strip=True)
        
        # Get all move containers in this section
        move_containers = h2.find_next_siblings('div', class_='moves')
        for moves_div in move_containers:
            for container in moves_div.find_all('div', class_='movecontainer'):
                move_data = {
                    'character': character_slug.capitalize(),
                    'section': current_section,
                }
                
                # Extract each field
                if movename := container.find('div', class_='movename'):
                    move_data['move'] = movename.get_text(strip=True)
                
                if startup := container.find('div', class_='startup'):
                    move_data['startup'] = startup.get_text(strip=True)
                
                if total := container.find('div', class_='totalframes'):
                    move_data['total_frames'] = total.get_text(strip=True)
                
                if landing := container.find('div', class_='landinglag'):
                    move_data['landing_lag'] = landing.get_text(strip=True)
                
                if notes := container.find('div', class_='notes'):
                    move_data['notes'] = notes.get_text(strip=True)
                
                if damage := container.find('div', class_='basedamage'):
                    move_data['damage'] = damage.get_text(strip=True)
                
                if shieldlag := container.find('div', class_='shieldlag'):
                    move_data['shield_lag'] = shieldlag.get_text(strip=True)
                
                if shieldstun := container.find('div', class_='shieldstun'):
                    move_data['shield_stun'] = shieldstun.get_text(strip=True)
                
                if hitbox_type := container.find('div', class_='whichhitbox'):
                    move_data['hitbox_type'] = hitbox_type.get_text(strip=True)
                
                if advantage := container.find('div', class_='advantage'):
                    move_data['advantage_on_shield'] = advantage.get_text(strip=True)
                
                if active := container.find('div', class_='activeframes'):
                    move_data['active_frames'] = active.get_text(strip=True)
                
                if endlag := container.find('div', class_='endlag'):
                    move_data['end_lag'] = endlag.get_text(strip=True)
                
                moves.append(move_data)
    
    df = pd.DataFrame(moves)
    return df


if __name__ == "__main__":
    df = scrape_character("mario")
    
    print(f"Scraped {len(df)} moves for Mario")
    print("\nPreview:")
    print(df[['section', 'move', 'startup', 'active_frames', 'damage', 'advantage_on_shield']].head(15))
    
    # Save
    df.to_csv("mario_moves.csv", index=False)
    print("\nSaved to mario_moves.csv")
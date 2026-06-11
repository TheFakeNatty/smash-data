# oos_analyzer.py
import sys
import pandas as pd
from pathlib import Path
import re

sys.path.append(str(Path(__file__).parent.parent))
from character.characters import CHARACTERS

def extract_oos_from_misc(df: pd.DataFrame) -> pd.DataFrame:
    """Extract Out of Shield options from Misc section."""
    oos_data = []
    
    for _, row in df[df['section'] == 'Misc Info'].iterrows():
        text = row.get('misc_raw', '') or row.get('notes', '')
        if not text:
            continue
            
        # Find patterns like "Out of Shield, Neutral Air — 6 frames"
        matches = re.findall(r'Out of Shield,\s*([^—]+?)\s*—\s*(\d+)', text)
        for move, frames in matches:
            oos_data.append({
                'character': row['character'],
                'oos_move': move.strip(),
                'oos_frames': int(frames),
                'source': 'misc'
            })
    
    return pd.DataFrame(oos_data)


def get_best_oos(character_name: str, raw_data_dir: Path = Path("data/raw")):
    """Get best OoS options for a character."""
    file_path = raw_data_dir / f"{character_name.lower().replace(' ', '_').replace('.', '')}_moves.csv"
    
    if not file_path.exists():
        # Try slug matching
        for char in CHARACTERS:
            if char.name.lower() == character_name.lower() or char.slug == character_name.lower():
                file_path = raw_data_dir / f"{char.slug}_moves.csv"
                break
    
    df = pd.read_csv(file_path)
    oos_df = extract_oos_from_misc(df)
    
    if oos_df.empty:
        return None
    
    best = oos_df.nsmallest(5, 'oos_frames')  # lowest frames = best
    return best


def compare_oos(char1: str, char2: str):
    """Compare best OoS options between two characters."""
    df1 = get_best_oos(char1)
    df2 = get_best_oos(char2)
    
    print(f"\n🔥 Best Out of Shield Options Comparison")
    print(f"{char1} vs {char2}\n")
    
    print(f"{char1}:")
    print(df1[['oos_move', 'oos_frames']].to_string(index=False))
    
    print(f"\n{char2}:")
    print(df2[['oos_move', 'oos_frames']].to_string(index=False))
    
    # Overall fastest
    combined = pd.concat([df1, df2])
    fastest = combined.nsmallest(3, 'oos_frames')
    print(f"\n🏆 Overall Fastest OoS: {fastest.iloc[0]['character']} with {fastest.iloc[0]['oos_move']} ({fastest.iloc[0]['oos_frames']}f)")
"""
Step 4: Tag each comment with one or more commercial themes.
Themes defined via multilingual keyword dictionaries (FR + EN + AR + Tunisian Arabizi).
"""
import pandas as pd
from collections import Counter

df = pd.read_csv('zynia_scored.csv', encoding='utf-8-sig')

themes = {
    'Price / Availability': [
        'prix', 'price', 'combien', 'cher', 'gadech', 'bgadech', '9addech',
        'be gadech', 'بقداش', 'سعر', 'magasin', 'win', 'mnin', 'pharmasi',
        'disponible', 'dispo', 'mawjod', 'mawjoda', 'mwjouda', 'commande',
        'commander', 'najem n3adi', 'cmandi', 'livraison'
    ],
    'Smell / Scent': [
        'odeur', 'parfum', 'sent', 'senteur', 'rihetha', 'ri7etha', 'smell',
        'scent', 'ريحة', 'ريحتها', 'bnina', 'pailletée', 'parfume'
    ],
    'Texture / Formula': [
        'texture', 'formula', 'gel', 'crème', 'creme', 'serum', 'sérum',
        'liquide', 'épais', 'épaisse', 'onctueux', 'léger', 'legere',
        'pailletée', 'paillette'
    ],
    'Effectiveness / Results': [
        'efficace', 'resultat', 'résultat', 'marche', 'fonctionne', 'works',
        'effect', 'ya3mel', 'mocha7eb', 'ta7seen', 'ameliore', 'amélioré',
        '9echra', 'taya7', 'ch3ar', 'chaar', 'cheveux', 'peau', 'skin',
        'bachra', 'wejhi'
    ],
    'Skin Compatibility': [
        'oily', 'dry', 'sensible', 'sensitive', 'acné', 'acne', 'bouton',
        'eczema', 'allergy', 'allergie', 'peau grasse', 'peau sèche',
        'tahsas', 'sahsasia', 'بشرة', 'حساسة', 'دهنية'
    ],
    'Natural Ingredients': [
        'naturel', 'natural', 'bio', 'organic', 'tabi3i', 'chimique',
        'ingredient', 'ingrédient', 'huile', 'extrait', 'aloe', 'concombre',
        'jasmin', 'olive'
    ],
    'Sun / Weather': [
        'soleil', 'chms', 'chams', 'chmes', 'sun', 'شمس', 'été', 'summer',
        'hiver', 'winter', 'spf', 'protection'
    ],
    'Store Experience': [
        'magasin', 'boutique', 'store', 'livraison', 'delivery', 'colis',
        'pharmasi', 'pharmacie'
    ],
    'Hair Care': [
        'cheveux', 'ch3ar', 'chaar', 'hair', 'curly', 'frisés', 'frisée',
        'شعر', 'taya7', 'lissant', 'volume'
    ],
    'Brand Love / Loyalty': [
        'nhebb', 'nheb', 'ma7leha', 'mahleha', 'love', 'adore', 'préféré',
        'préférée', 'top', 'best', 'meilleur', 'parfait', 'merci', 'bravo',
        'yar7em weldikom', 'inshallah', 'rabi', 'yarabi'
    ],
}

def tag_themes(text):
    t = str(text).lower()
    return [theme for theme, keywords in themes.items() if any(kw.lower() in t for kw in keywords)]

df['themes'] = df['text_clean'].apply(tag_themes)

all_themes = [t for sublist in df['themes'] for t in sublist]
theme_counts = Counter(all_themes)

print("Theme frequency:")
for theme, count in theme_counts.most_common():
    pct = count / len(df) * 100
    print(f"  {theme:30s} {count:4d}  ({pct:.1f}%)")

print("\nTheme by sentiment:")
theme_sentiment = []
for _, row in df.iterrows():
    for theme in row['themes']:
        theme_sentiment.append({'theme': theme, 'sentiment': row['sentiment']})

ts_df = pd.DataFrame(theme_sentiment)
if len(ts_df) > 0:
    print(pd.crosstab(ts_df['theme'], ts_df['sentiment']).sort_values('positive', ascending=False))

df.to_csv('zynia_themed.csv', index=False, encoding='utf-8-sig')
print(f"\nSaved as zynia_themed.csv")
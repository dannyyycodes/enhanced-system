"""
Idea Bank
=========
All your animal and baby video ideas
"""

IDEAS = [
    {
        "slug": "baby-goat-happy-hops",
        "language": "en",
        "coreHook": "A newborn baby goat does tiny excited hops around a camera placed on the grass.",
        "settingHints": "Small farm field at golden hour.",
        "coreCharacters": "One tiny newborn goat kid.",
        "coreAction": "Goat hops in energetic, clumsy bursts around the camera, occasionally sliding or stumbling cutely.",
        "safetyConstraints": "Gentle terrain with no obstacles.",
        "styleTags": ["goat", "baby-animal", "nature", "playful", "viral"]
    },
    {
        "slug": "baby-husky-mimic-sounds",
        "language": "en",
        "coreHook": "A baby babbles, and a husky puppy tries to mimic the baby's sounds.",
        "settingHints": "Indoor nursery with warm window light.",
        "coreCharacters": "One baby sitting, one husky puppy facing them.",
        "coreAction": "Baby babbles. Husky pup responds with tiny attempts at howling, tilting its head in confusion.",
        "safetyConstraints": "Puppy must be gentle and stable.",
        "styleTags": ["baby", "husky", "talking", "cute", "sound-mimic"]
    },
    {
        "slug": "baby-elephant-curious-trunk",
        "language": "en",
        "coreHook": "A baby elephant gently explores a camera lens with its tiny trunk.",
        "settingHints": "Sanctuary environment with soft dust and sunlight.",
        "coreCharacters": "One young baby elephant.",
        "coreAction": "Elephant taps and explores the camera with its trunk, then sneezes a tiny dust puff.",
        "safetyConstraints": "Elephant must act gentle. No dangerous trunk swings.",
        "styleTags": ["elephant", "baby-animal", "nature", "viral", "cute"]
    },
    {
        "slug": "baby-kitten-soft-paws",
        "language": "en",
        "coreHook": "A tiny kitten kneads on the baby's blanket, mesmerising the baby.",
        "settingHints": "Indoor blanket scene with close smartphone angle.",
        "coreCharacters": "One baby lying on back, one kitten near feet.",
        "coreAction": "Kitten kneads the blanket gently. Baby reaches out curiously.",
        "safetyConstraints": "Kitten must be gentle. No claws extended.",
        "styleTags": ["baby", "kitten", "kneading", "adorable", "viral"]
    },
    {
        "slug": "baby-sloth-slow-hug",
        "language": "en",
        "coreHook": "A baby sloth slowly crawls toward the camera and hugs it.",
        "settingHints": "Rescue center, natural wood branches, soft lighting.",
        "coreCharacters": "One baby sloth.",
        "coreAction": "Sloth crawls slowly, then wraps its arms around the camera with an innocent expression.",
        "safetyConstraints": "Sloth kept low and safe.",
        "styleTags": ["sloth", "baby-animal", "hug", "adorable"]
    },
    {
        "slug": "fawn-curious-head-tilt",
        "language": "en",
        "coreHook": "A newborn fawn hears a soft sound and tilts its head repeatedly.",
        "settingHints": "Forest edge or sanctuary meadow.",
        "coreCharacters": "One newborn fawn.",
        "coreAction": "Fawn tilts head slowly left and right, then steps forward shyly.",
        "safetyConstraints": "Soft terrain, calm environment.",
        "styleTags": ["fawn", "baby-animal", "cute", "nature"]
    },
    {
        "slug": "baby-penguin-tiny-waddle",
        "language": "en",
        "coreHook": "A baby penguin waddles toward the camera and slips gently on its belly.",
        "settingHints": "Indoor cool habitat with soft ice or snow texture.",
        "coreCharacters": "One fluffy penguin chick.",
        "coreAction": "Penguin waddles, slips, slides forward, then looks proud.",
        "safetyConstraints": "No sharp ice. Safe ground.",
        "styleTags": ["penguin", "cute", "baby-animal", "slip", "viral"]
    },
    {
        "slug": "hedgehog-tiny-sniff",
        "language": "en",
        "coreHook": "A baby hedgehog sniffs the camera lens repeatedly, twitching its tiny nose.",
        "settingHints": "Soft wooden table or blanket.",
        "coreCharacters": "One very small hedgehog.",
        "coreAction": "Hedgehog sniffs and wiggles toward the lens, then curls into a tiny ball.",
        "safetyConstraints": "Safe padded surface.",
        "styleTags": ["hedgehog", "cute", "micro", "sniff", "viral"]
    },
    {
        "slug": "baby-lab-puppy-tug",
        "language": "en",
        "coreHook": "A baby and a Labrador puppy gently tug on opposite sides of a soft cloth.",
        "settingHints": "Living room play mat with natural window light.",
        "coreCharacters": "One baby, one lab puppy.",
        "coreAction": "Baby pulls cloth. Puppy pulls the other side in tiny, playful motions.",
        "safetyConstraints": "No rough tugging. Baby must remain stable.",
        "styleTags": ["baby", "puppy", "lab", "playful"]
    },
    {
        "slug": "baby-chimp-curious-hands",
        "language": "en",
        "coreHook": "A baby chimp explores the camera gently with its hands.",
        "settingHints": "Sanctuary habitat with soft leaves.",
        "coreCharacters": "One baby chimp.",
        "coreAction": "Chimp touches lens with curiosity, then mimics the camera operator.",
        "safetyConstraints": "Chimp must remain gentle, slow, safe.",
        "styleTags": ["chimp", "baby-animal", "cute"]
    }
]


def get_next_idea(current_index: int = 0):
    """Get the next idea in rotation"""
    index = current_index % len(IDEAS)
    return IDEAS[index], (index + 1) % len(IDEAS)


def get_random_idea():
    """Get a random idea"""
    import random
    return random.choice(IDEAS)


def get_idea_by_slug(slug: str):
    """Get specific idea by slug"""
    for idea in IDEAS:
        if idea['slug'] == slug:
            return idea
    return None


def add_custom_idea(idea_data: dict):
    """Add a custom idea to the bank"""
    IDEAS.append(idea_data)
    return len(IDEAS) - 1

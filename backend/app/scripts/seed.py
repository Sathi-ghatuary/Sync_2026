"""
Database seeding script with sample Indian newspaper/publication titles.
Use this to initialize the database with sample data for testing.
"""
from ..db.manager import get_db_manager


def seed_database():
    """Populate database with sample Indian publication titles."""
    db_manager = get_db_manager()
    
    sample_titles = [
        # Major English newspapers
        "The Times of India",
        "The Indian Express",
        "The Hindu",
        "Hindustan Times",
        "Deccan Herald",
        "The Statesman",
        "The Telegraph",
        "The Asian Age",
        "DNA",
        "Mid Day",
        "The News18",
        "India Today",
        "Outlook",
        "The Week",
        "Tehelka",
        "Business Standard",
        "Mint",
        "The Economic Times",
        "Financial Express",
        "The Pioneer",
        "Daily Pioneer",
        "Dainik Jagran",
        "Amar Ujala",
        "Rajasthan Patrika",
        "Gujarat Samachar",
        "Navbharat Times",
        "Danik Bhaskar",
        "Sandhya Times",
        "Evening Herald",
        "Morning Chronicle",
        "Daily News Summary",
        "Weekly Digest",
        "News India",
        "India News Today",
        "National Gazette",
        "Press Bureau",
        "Daily Express Media",
        "Indian Chronicle",
        "National Daily",
        "Prime News",
        "Top Stories Daily",
        "Breaking News Times",
        "Current Affairs Weekly",
        "Political Voice",
        "Sports Daily News",
        "Business Chronicle",
        "Technology Today",
        "Entertainment Weekly",
        "Lifestyle Magazine",
        "Health and Wellness Daily",
    ]
    
    print(f"Seeding database with {len(sample_titles)} sample titles...")
    count = db_manager.batch_add_titles(sample_titles)
    print(f"Successfully seeded {count} titles")
    
    stats = db_manager.get_stats()
    print(f"\nDatabase stats:")
    print(f"  Total titles: {stats['total_titles']}")
    print(f"  Total applications: {stats['total_applications']}")


if __name__ == "__main__":
    seed_database()

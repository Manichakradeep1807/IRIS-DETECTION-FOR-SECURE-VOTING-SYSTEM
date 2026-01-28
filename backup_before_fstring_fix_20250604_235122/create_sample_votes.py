#!/usr/bin/env python3
"""
Create Sample Voting Data
Adds sample votes to demonstrate the voting system
"""

from voting_system import voting_system

def create_sample_votes():
    """Create sample votes for demonstration"""
    
    # Sample votes from different persons to different parties
    sample_votes = [
        (1, 1, 0.95),   # Person 1 → Democratic Party
        (2, 2, 0.88),   # Person 2 → Republican Party  
        (3, 1, 0.92),   # Person 3 → Democratic Party
        (4, 3, 0.85),   # Person 4 → Green Party
        (5, 2, 0.91),   # Person 5 → Republican Party
        (6, 4, 0.87),   # Person 6 → Libertarian Party
        (7, 1, 0.94),   # Person 7 → Democratic Party
        (8, 5, 0.89),   # Person 8 → Independent
        (9, 2, 0.86),   # Person 9 → Republican Party
        (10, 3, 0.93),  # Person 10 → Green Party
        (11, 1, 0.96),  # Person 11 → Democratic Party
        (12, 6, 0.84),  # Person 12 → Socialist Party
        (13, 2, 0.90),  # Person 13 → Republican Party
        (14, 1, 0.88),  # Person 14 → Democratic Party
        (15, 3, 0.92),  # Person 15 → Green Party
        (16, 4, 0.85),  # Person 16 → Libertarian Party
        (17, 1, 0.93),  # Person 17 → Democratic Party
        (18, 2, 0.87),  # Person 18 → Republican Party
        (19, 5, 0.91),  # Person 19 → Independent
        (20, 1, 0.89),  # Person 20 → Democratic Party
    ]
    
    print("Creating sample voting data...")
    print("=" * 40)
    
    parties = voting_system.get_parties()
    party_names = {p['id']: p['name'] for p in parties}
    
    votes_created = 0
    votes_skipped = 0
    
    for person_id, party_id, confidence in sample_votes:
        if not voting_system.has_voted(person_id):
            success = voting_system.cast_vote(person_id, party_id, confidence)
            if success:
                votes_created += 1
                party_name = party_names.get(party_id, "Party {}".format(party_id))
                print("✅ Person {} voted for {}".format(person_id, party_name))
            else:
                print("❌ Failed to record vote for Person {}".format(person_id))
        else:
            votes_skipped += 1
            print("⏭️ Person {} already voted".format(person_id))
    
    print("\n" + "=" * 40)
    print("📊 SUMMARY:")
    print("   Votes created: {}".format(votes_created))
    print("   Votes skipped: {}".format(votes_skipped))

    # Show current results
    results = voting_system.get_voting_results()
    print("\n📈 CURRENT VOTING STATISTICS:")
    print("   Total votes: {}".format(results['total_votes']))
    print("   Total voters: {}".format(results['total_voters']))
    print("   Turnout: {:.1f}%".format((results['total_voters'] / 108) * 100))

    print("\n🏆 CURRENT STANDINGS:")
    for result in sorted(results['results'], key=lambda x: x['votes'], reverse=True):
        if result['votes'] > 0:
            print(f"   {result['symbol']} {result['party']}: {result['votes']} votes ({result['percentage']:.1f}%)")
    
    return votes_created

if __name__ == "__main__":
    create_sample_votes()

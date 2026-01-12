# explore_schema.py
"""
Analyze and explore the CS-KG schema.
This script provides insights into the knowledge graph structure directly from the CSV file.

Usage:
    python explore_schema.py
"""


import pandas as pd
from collections import Counter, defaultdict

def load_and_analyze_schema(csv_path):
    """Load and analyze the knowledge graph schema."""
    print("Loading triples from CSV...")
    df = pd.read_csv(csv_path)
    
    print(f"\n{'='*80}")
    print("CS-KG SCHEMA ANALYSIS")
    print(f"{'='*80}\n")
    
    # Basic statistics
    print("📊 BASIC STATISTICS:")
    print(f"   Total triples: {len(df):,}")
    print(f"   Unique subjects: {df['subj'].nunique():,}")
    print(f"   Unique objects: {df['obj'].nunique():,}")
    print(f"   Unique relations: {df['rel'].nunique():,}")
    
    # Get all unique entities
    all_entities = set(df['subj'].unique()) | set(df['obj'].unique())
    print(f"   Total unique entities: {len(all_entities):,}")
    
    # Entity types analysis
    print(f"\n🏷️  ENTITY TYPES:")
    subj_types = Counter(df['subj_type'])
    obj_types = Counter(df['obj_type'])
    all_types = Counter()
    all_types.update(subj_types)
    all_types.update(obj_types)
    
    print(f"\n   Subject Types Distribution:")
    for etype, count in subj_types.most_common(15):
        print(f"      {etype:30s}: {count:,}")
    
    print(f"\n   Object Types Distribution:")
    for etype, count in obj_types.most_common(15):
        print(f"      {etype:30s}: {count:,}")
    
    print(f"\n   Combined Entity Types (Top 20):")
    for etype, count in all_types.most_common(20):
        print(f"      {etype:30s}: {count:,}")
    
    # Relations analysis
    print(f"\n🔗 RELATIONS:")
    relations = Counter(df['rel'])
    print(f"   Total unique relations: {len(relations)}")
    print(f"\n   Top 40 Relations:")
    for rel, count in relations.most_common(40):
        print(f"      {rel:50s}: {count:,}")
    
    # Type-Relation-Type patterns (Schema patterns)
    print(f"\n🔀 SCHEMA PATTERNS (Subject Type → Relation → Object Type):")
    patterns = Counter(zip(df['subj_type'], df['rel'], df['obj_type']))
    print(f"\n   Top 30 patterns:")
    for (s_type, rel, o_type), count in patterns.most_common(30):
        print(f"      {s_type:20s} --[{rel:30s}]--> {o_type:20s}  ({count:,} occurrences)")
    
    # Source analysis
    print(f"\n📚 EXTRACTION SOURCES:")
    source_counts = Counter()
    for sources_str in df['sources']:
        try:
            sources = eval(sources_str) if isinstance(sources_str, str) else sources_str
            for source in sources:
                source_counts[source] += 1
        except:
            pass
    
    print(f"   Triples by extraction source:")
    for source, count in source_counts.most_common():
        print(f"      {source:30s}: {count:,}")
    
    # Support distribution
    print(f"\n💪 SUPPORT DISTRIBUTION:")
    print(f"   Min support: {df['support'].min()}")
    print(f"   Max support: {df['support'].max()}")
    print(f"   Mean support: {df['support'].mean():.2f}")
    print(f"   Median support: {df['support'].median():.0f}")
    
    support_dist = df['support'].value_counts().sort_index()
    print(f"\n   Support count distribution:")
    for support in range(1, min(11, df['support'].max() + 1)):
        if support in support_dist.index:
            count = support_dist[support]
            print(f"      Support = {support}: {count:,} triples")
    
    # Source length distribution
    print(f"\n📏 SOURCE LENGTH DISTRIBUTION:")
    source_len_dist = df['source_len'].value_counts().sort_index()
    print(f"   Number of extraction sources per triple:")
    for src_len, count in source_len_dist.items():
        print(f"      {src_len} source(s): {count:,} triples")
    
    # Sample triples by type
    print(f"\n📋 SAMPLE TRIPLES BY ENTITY TYPE:")
    for etype in all_types.most_common(5):
        etype_name = etype[0]
        samples = df[df['subj_type'] == etype_name].head(5)
        if len(samples) > 0:
            print(f"\n   {etype_name}:")
            for _, row in samples.iterrows():
                sources = eval(row['sources']) if isinstance(row['sources'], str) else row['sources']
                sources_str = ', '.join(list(sources)[:2])
                print(f"      {row['subj'][:40]:40s} --[{row['rel']:20s}]--> {row['obj'][:40]:40s} [{sources_str}]")
    
    # High-support triples
    print(f"\n⭐ HIGHEST SUPPORT TRIPLES (Top 25):")
    top_triples = df.nlargest(25, 'support')
    for _, row in top_triples.iterrows():
        sources = eval(row['sources']) if isinstance(row['sources'], str) else row['sources']
        print(f"      [support={row['support']:2d}] {row['subj'][:35]:35s} --[{row['rel']:20s}]--> {row['obj'][:35]:35s}")
        print(f"                   Types: {row['subj_type']:15s} → {row['obj_type']:15s} | Sources: {', '.join(list(sources))}")
    
    # Specific relation types analysis
    print(f"\n🔬 ANALYSIS BY RELATION TYPE:")
    
    # DyGIE++ style relations
    dygiepp_rels = ['USED-FOR', 'PART-OF', 'HYPONYM-OF', 'FEATURE-OF', 'CONJUNCTION', 'COMPARE', 'EVALUATE-FOR']
    print(f"\n   DyGIE++ Relations:")
    for rel in dygiepp_rels:
        count = len(df[df['rel'] == rel])
        if count > 0:
            print(f"      {rel:20s}: {count:,}")
            samples = df[df['rel'] == rel].head(3)
            for _, row in samples.iterrows():
                print(f"         {row['subj'][:30]:30s} → {row['obj'][:30]}")
    
    # Hierarchical relations
    print(f"\n   Hierarchical Relations:")
    hier_rels = df[df['rel'].str.contains('hyponym|broader|is-a|subclass', case=False, na=False)]
    if len(hier_rels) > 0:
        print(f"      Total: {len(hier_rels):,}")
        for _, row in hier_rels.head(5).iterrows():
            print(f"         {row['subj'][:30]:30s} --[{row['rel']}]--> {row['obj'][:30]}")
    
    print(f"\n{'='*80}\n")
    
    return df


def export_stats_to_file(df, output_file='schema_stats.txt'):
    """Export detailed statistics to a text file."""
    with open(output_file, 'w', encoding='utf-8') as f:
        # Redirect output
        import sys
        old_stdout = sys.stdout
        sys.stdout = f
        
        load_and_analyze_schema(df)
        
        sys.stdout = old_stdout
    
    print(f"✅ Statistics exported to {output_file}")


def find_entity_connections(df, entity_name):
    """Find all connections for a specific entity."""
    print(f"\n🔍 Connections for entity: '{entity_name}'")
    print("="*80)
    
    # As subject
    as_subj = df[df['subj'].str.contains(entity_name, case=False, na=False)]
    print(f"\nAs SUBJECT ({len(as_subj)} triples):")
    for _, row in as_subj.head(10).iterrows():
        print(f"   {row['subj']} --[{row['rel']}]--> {row['obj']}")
    
    # As object
    as_obj = df[df['obj'].str.contains(entity_name, case=False, na=False)]
    print(f"\nAs OBJECT ({len(as_obj)} triples):")
    for _, row in as_obj.head(10).iterrows():
        print(f"   {row['subj']} --[{row['rel']}]--> {row['obj']}")


def interactive_explore(df):
    """Interactive exploration mode."""
    print("\n" + "="*80)
    print("INTERACTIVE EXPLORATION MODE")
    print("="*80)
    print("\nCommands:")
    print("  1. Search for entity: type 'search <entity_name>'")
    print("  2. Filter by type: type 'type <entity_type>'")
    print("  3. Filter by relation: type 'rel <relation_name>'")
    print("  4. Show stats: type 'stats'")
    print("  5. Exit: type 'quit'")
    
    while True:
        try:
            cmd = input("\n> ").strip()
            
            if cmd.lower() == 'quit':
                break
            elif cmd.lower() == 'stats':
                load_and_analyze_schema(df)
            elif cmd.lower().startswith('search '):
                entity = cmd[7:].strip()
                find_entity_connections(df, entity)
            elif cmd.lower().startswith('type '):
                etype = cmd[5:].strip()
                filtered = df[(df['subj_type'] == etype) | (df['obj_type'] == etype)]
                print(f"\nFound {len(filtered)} triples with entity type '{etype}':")
                for _, row in filtered.head(20).iterrows():
                    print(f"   {row['subj'][:35]:35s} --[{row['rel']:20s}]--> {row['obj'][:35]}")
            elif cmd.lower().startswith('rel '):
                rel = cmd[4:].strip()
                filtered = df[df['rel'].str.contains(rel, case=False, na=False)]
                print(f"\nFound {len(filtered)} triples with relation matching '{rel}':")
                for _, row in filtered.head(20).iterrows():
                    print(f"   {row['subj'][:35]:35s} --[{row['rel']:20s}]--> {row['obj'][:35]}")
            else:
                print("Unknown command. Try 'stats', 'search <entity>', 'type <type>', 'rel <relation>', or 'quit'")
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    CSV_PATH = "./construction/cskg_data/cskg_triples.csv"
    
    # Load and analyze
    df = load_and_analyze_schema(CSV_PATH)

    export_stats_to_file(CSV_PATH)
    
    # Ask if user wants interactive mode
    print("\nWould you like to enter interactive exploration mode? (y/n): ", end='')
    try:
        choice = input().strip().lower()
        if choice == 'y':
            interactive_explore(df)
    except:
        pass
    
    print("\n✅ Analysis complete!")
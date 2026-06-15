import chromadb


def inspect_chromadb():
    """Inspect all documents and metadata stored in ChromaDB."""
    client = chromadb.PersistentClient(path="chroma_db")
    collection = client.get_or_create_collection(name="pdf_chunks")
    
    # Get all documents (no filter)
    all_data = collection.get()
    
    print("=" * 80)
    print("CHROMADB INSPECTION REPORT")
    print("=" * 80)
    print(f"\nTotal documents stored: {len(all_data['ids'])}\n")
    
    # Group by source
    sources = {}
    for i, doc_id in enumerate(all_data['ids']):
        metadata = all_data['metadatas'][i]
        source = metadata.get('source', 'UNKNOWN')
        
        if source not in sources:
            sources[source] = []
        sources[source].append({
            'id': doc_id,
            'metadata': metadata
        })
    
    # Print by source
    for source in sorted(sources.keys()):
        docs = sources[source]
        print(f"\nSource: '{source}' ({len(docs)} chunks)")
        print("-" * 80)
        for doc in docs[:3]:  # Show first 3 chunks per source
            print(f"  ID: {doc['id']}")
            print(f"  Metadata: {doc['metadata']}")
        if len(docs) > 3:
            print(f"  ... and {len(docs) - 3} more chunks")
    
    print("\n" + "=" * 80)
    print("METADATA VALUES (Unique sources):")
    print("=" * 80)
    for source in sorted(sources.keys()):
        print(f"  - '{source}' (repr: {repr(source)})")
    
    print("\n" + "=" * 80)
    print("TESTING QUERIES:")
    print("=" * 80)
    
    for source in sorted(sources.keys()):
        query_result = collection.get(
            where={"source": {"$eq": source}}
        )
        count = len(query_result['ids'])
        print(f"  Query with source='{source}': {count} results")


if __name__ == "__main__":
    inspect_chromadb()

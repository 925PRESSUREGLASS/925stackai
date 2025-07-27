from quote_embedder import QuoteVectorStore

# Build the index (if not already built)
store = QuoteVectorStore()
store.build_index()

# Test a query
results = store.query("Clean 10 windows on a two storey house")
print("Query results:", results)
print("Vector count:", store.count())

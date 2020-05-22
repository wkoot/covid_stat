def iter_chunks(lst, n):
    """Yield successive n-sized chunks from lst, tnx Ned Batchelder"""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def check_pipeline_methods(pipeline):
    if hasattr(pipeline, "open_spider") and \
        hasattr(pipeline, "close_spider") and hasattr(pipeline, "process_item"):
        return True
    else:
        return False
        

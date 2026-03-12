# hadoop/__init__.py
# Hadoop/HDFS utilities for AI Data Engineer Assistant
from hadoop.hdfs_client import HdfsClient, upload_to_hdfs, get_hdfs_or_local

__all__ = ["HdfsClient", "upload_to_hdfs", "get_hdfs_or_local"]
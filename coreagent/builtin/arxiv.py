from typing import Optional

from .filetool import FileTool

import requests
import feedparser

# NOTE: This tool requires feedparser to be installed. 

class ArxivTool:
    def __init__(self, file_tool_for_root: Optional[FileTool] = None, enable_download: bool = True):
      """
      file_tool: If not None, download_arxiv_paper_pdf will use FileTool dir as root dir.
      """
      self._file_tool_for_root = file_tool_for_root
      self._enable_download = enable_download
    def arxiv_api_query(self, search_query: str, start: int, max_results: int) -> dict:
        """
        # Query ARXIV for papers matching search_query
        search_query: "URL-escaped query string"
        start: "Start index as offset, can be used for paging. "
        max_results: "Results returned. "
        """
        base_url = 'http://export.arxiv.org/api/query'
        params = {
            'search_query': search_query,
            'start': start,
            'max_results': max_results
        }
        
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            feed = feedparser.parse(response.text)
            
            results = {
                'entries': [],
                'total_results': int(feed.feed.opensearch_totalresults),
                'start_index': int(feed.feed.opensearch_startindex),
                'items_per_page': int(feed.feed.opensearch_itemsperpage)
            }
            
            for entry in feed.entries:
                results['entries'].append({
                    'title': entry.title,
                    'summary': entry.summary,
                    'link': entry.link,
                    'arxiv_id': entry.id.split('/abs/')[-1],
                    'categories': [cat.term for cat in entry.tags],
                    'published': entry.published
                })
                
            return results
            
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}
    def download_arxiv_paper_pdf(self, arxiv_id: str, save_path: str):
        """
        # Download a paper PDF to designated location.
        arxiv_id: "The paper ID you queried from arxiv_api_query tool. "
        save_path: "The file to save at. "
        """
        if not self._enable_download:
            return {'error': 'Download is disabled for this tool. '}
        try:
            response = requests.get("https://arxiv.org/pdf/" + arxiv_id)
            response.raise_for_status()
            if self._file_tool_for_root is not None:
              save_path = self._file_tool_for_root._resolve(save_path)
              if save_path is None:
                  return {'error': f'File path {save_path} is not allowed to be accessed. '}
            with open(save_path, 'wb') as file:
                file.write(response.content)
            return {'message': f'Paper {arxiv_id} downloaded successfully. '}
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}

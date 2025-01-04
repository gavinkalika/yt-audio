from pathlib import Path
from typing import Optional, List
from dataclasses import dataclass
import logging
from concurrent.futures import ThreadPoolExecutor
import yt_dlp
from pydub import AudioSegment
import sys

@dataclass
class DownloadResult:
    """Data class to store download results"""
    url: str
    success: bool
    filepath: Optional[Path] = None
    error: Optional[str] = None

@dataclass
class InputModel:
    url: str

class InputHandler:
    def __init__(self, inputs: list[str]):
        if (len(inputs) == 0):
            raise ValueError("No inputs provided")
        self.inputs = inputs
        
    def get_inputs(self) -> list[InputModel]:
        return [InputModel(url=input) for input in self.inputs]


class YouTubeAudioExtractor:
    """Extract audio from YouTube videos using modern Python practices"""

    def __init__(self, output_dir: str | Path = "downloads", inputs: list[InputModel] = []):
        self.output_dir = Path(output_dir)
        self._setup_logging()
        self._setup_download_options()
        self.inputs = [input.url for input in inputs] # this uses list comprehension and transformations!
        print( self.inputs )
        # sys.exit() used for debugging purposes

    def _setup_logging(self) -> None:
        """Configure logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.logger = logging.getLogger(__name__)

    def _setup_download_options(self) -> None:
        """Configure yt-dlp options"""
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': str(self.output_dir / '%(title)s.%(ext)s'),
            'verbose': False,
            'quiet': False,
            'no_warnings': True
        }

    def extract_batch(self, max_workers: int = 3) -> list[DownloadResult]:
        """
        Extract audio from multiple YouTube URLs concurrently

        Args:
            urls: List of YouTube video URLs
            max_workers: Maximum number of concurrent downloads

        Returns:
            List of DownloadResult objects
        """
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(self.extract_single, self.inputs ))
        return results

def main() -> None:
    inputs = InputHandler(sys.argv[1:])
    inputs = inputs.get_inputs()
    extractor = YouTubeAudioExtractor(output_dir="youtube_audio", inputs=inputs)

    extractor.extract_batch(max_workers=3)


if __name__ == "__main__":
    main()

import json
import logging
import os
from pathlib import Path

import httpx
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


def to_json(data: dict, league: str, year: str):
    filename = f"initial_{year}"
    root = Path(__file__).resolve().parent.parent
    path = (root/"data"/"raw"/"football_data"/league/year/f"{filename}.json")
    try:
        path.parent.mkdir(parents=True, exist_ok=True)

        # Create file only if it does not exist
        with path.open("x", encoding="utf-8") as fp:
            json.dump(
                data,
                fp,
                sort_keys=True,
                indent=4,
                ensure_ascii=False
            )

        logger.info("Successfully saved data to %s", path)

    except FileExistsError: 
        logger.warning("File already exists. %s", path)
        raise 
    except PermissionError:
        logger.exception("Permission denied when writing to %s", path)
        raise 
    except OSError:
        logger.exception("File system error when writing to %s", path)
        raise 
    except (TypeError, ValueError):
        logger.exception("Error serializing data to JSON")
        raise 


def extract_data(year: str, competition: str):
    """Fetch football data from football-data.org and save it as JSON."""

    # Load environment variables
    load_dotenv()

    token = os.getenv("API_TOKEN")

    # Check API token
    if not token:
        logger.error("API_TOKEN is missing. Check your .env file.")
        return

    headers = {"X-Auth-Token": token}

    address = (
        f"https://api.football-data.org/v4/competitions/"
        f"{competition}/matches?season={year}"
    )

    logger.info("Requesting data from %s", address)

    try:
        # Make HTTP request
        with httpx.Client(timeout=10.0) as client:
            response = client.get(address, headers=headers)

            # Check HTTP status code
            response.raise_for_status()

            # Parse JSON response
            data = response.json()
            print("--------", len(data["matches"]))
            
        logger.info("Successfully retrieved data from API.")

        # Save response
        to_json(data, competition, year)

    except httpx.TimeoutException:
        logger.error("Request timed out. API did not respond in time.")

    except httpx.ConnectError:
        logger.error("Could not connect to football-data.org.")

    except httpx.HTTPStatusError as e:
        status_code = e.response.status_code

        if status_code == 401:
            logger.error("Unauthorized: Invalid API token.")

        elif status_code == 403:
            logger.error("Forbidden: Access to this resource is denied.")

        elif status_code == 404:
            logger.error("Resource not found. Check competition and year.")

        elif status_code == 429:
            logger.error("Rate limit exceeded. Too many API requests.")

        elif status_code >= 500:
            logger.error("Server error at football-data.org: %s", status_code)

        else:
            logger.error("HTTP error occurred: %s", status_code)

    except httpx.RequestError as e:
        logger.error("Network error occurred: %s", e)

    except json.JSONDecodeError:
        logger.error("API response is not valid JSON.")
    
    except (OSError, ValueError, TypeError) as e:
        logger.error("Error saving JSON data: %s", e)

    except Exception:
        logger.exception("Unexpected error occurred.")


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    years = ["2023", "2024", "2025", "2026"]
    league = "BL1"
    for year in years:
        extract_data(year, league)
        
        

    




if __name__ == "__main__":
    main()

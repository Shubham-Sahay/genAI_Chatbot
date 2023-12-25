# Amazon Book Reviews Chatbot

This project is a chatbot designed to query Amazon book review data using natural language over an SQL database. The chatbot interacts with two tables: `books_data` and `books_ratings`. It prompts users for queries, generates corresponding SQL queries, executes them on the database, and synthesizes the results in natural language. The implementation utilizes Google Gemini Pro as the large language model (LLM) and the llamaindex framework.

## Setup

1. Clone the repository:

    ```bash
    git clone <repository-url>
    ```

2. Create a virtual environment using the provided `requirements.txt`:

    ```bash
    cd amazon-book-reviews-chatbot
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3. Create an SQLite database and set up tables:

    ```bash
    sqlite3 amazon_reviews.db
    ```

    ```sql
    -- Inside the SQLite shell
    CREATE TABLE books_data (
        book_id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        -- Add other columns as needed
    );

    CREATE TABLE books_ratings (
        book_id INTEGER PRIMARY KEY,
        rating INTEGER NOT NULL,
        -- Add other columns as needed
    );
    ```

4. Activate the environment and run the application:

    ```bash
    chainlit run main.py
    ```

    The application will be hosted on `localhost:8000`. Access the user interface to start querying the database.

## Usage

1. Enter natural language queries in the provided UI.
2. The chatbot generates corresponding SQL queries and executes them on the database.
3. The results are synthesized in natural language and displayed along with the SQL query.

## Notes

- Changes to the `.gitignore` file only affect future commits; they won't remove files already tracked by Git.
- To untrack and remove a file already committed, use the following commands:

    ```bash
    git rm --cached file_name.txt
    git commit -m "Remove file_name.txt from tracking"
    git push origin master
    ```

## Example Interaction:
- Show me rows of books_data table
- Show 5 rows with all columns of books_rating table
- List top 5 authors based on number of books published
- List books which are priced less than 99 dollars
- List top 5 most expensive books
- List out top 5 authors name by average rating(join books_data and books_rating tables)
- Show some highly rated books on science fiction
- Show some highly rated books on education
- Christopher has given how many reviews?
- Show some of the reviews of Christopher
- List out top 5 authors of most costliest books(join books_data and books_rating tables)


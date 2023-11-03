import time
import urllib.error
from bs4 import BeautifulSoup
from urllib.request import urlopen

"""
Manages html data
"""


class Parser:

    """
    Try something with get.text()
    """

    def http_error_handler(self, url):
        """
        Handles errors from accessing an url
        :param url: the url to access
        :return: the webpage's bytes
        """

        MAX_ATTEMPTS = 5

        # Error types
        TOO_MANY_REQUESTS = 429
        GATEWAY_TIMEOUT = 504

        for i in range(1, MAX_ATTEMPTS):
            try:
                return urlopen(url, timeout=20).read()

            except urllib.error.HTTPError as error:
                if error.code == TOO_MANY_REQUESTS:
                    print(f"Error 429, too many requests. Retry number {i}")
                    time.sleep(20)

                elif error.code == GATEWAY_TIMEOUT:
                    print(f"Error 504, gateway timeout. Retry number {i}")
                    time.sleep(20)
        raise ValueError("Exceeded max attempts. Rerun the program")

    def get_page_data_file(self, url, filename):
        """
        Writes a webpage's html to a file
        :param url: the url of the page to access
        :param filename: the file to write the html to
        """

        webpage = self.http_error_handler(url)
        with open(filename, "wb") as writer:
            writer.write(webpage)

    def get_page_data(self, url):
        """
        Returns the html data from a page
        :param url: the url of the page to access
        :return: html data of the url
        """

        return self.http_error_handler(url)

    def create_soup_file(self, filename):
        """
        Creates a BeautifulSoup object from a file
        :param filename: the file to create soup from
        :return: BeautifulSoup object of the file's html
        """

        with open(filename, "rb") as reader:
            return BeautifulSoup(reader, "html.parser")

    def create_soup(self, webpage):
        """
        Creates a BeautifulSoup object from a webpage
        :param webpage: the page to create soup from
        :return: BeautifulSoup object of the webpage's html
        """

        return BeautifulSoup(webpage, "html.parser")

    def get_post_links(self, soup):
        """
        Gets the links of all posts
        :param soup: soup object to parse
        :return: list of all post links on page
        """

        posts = []
        num_pinned_posts = self.find_num_pinned(soup)

        for link in soup.find_all('a'):
            link = str(link.get('href'))
            if "/comments/" in link and "old.reddit.com" in link:
                posts.append(link)

        return posts[num_pinned_posts:4]

    def find_num_pinned(self, soup):
        """
        Finds the number of pinned posts on a page
        :param soup: soup object to parse
        :return: int amount of pinned posts
        """

        num_pinned_posts = 0
        parent_div_class = "entry unvoted"
        announcement_title = "selected by this subreddit's moderators"

        post_parent_div = soup.find_all("div", class_=parent_div_class)
        for child_div in post_parent_div:
            if len(child_div.find_all_next(title=announcement_title)) > 0:
                num_pinned_posts += 1

        return num_pinned_posts

    def get_title(self, soup):
        """
        Gets the title of a post from a soup object
        :param soup: the soup of a post
        :return: the title of the post
        """

        title_tags_list = soup.find_all("title")

        if len(title_tags_list) != 1:
            raise ValueError("The get_title() function did not find a title.")

        unformatted_title_text = title_tags_list[0].get_text()

        colon_index = unformatted_title_text.rfind(" : ")
        formatted_title_text = unformatted_title_text[:colon_index]

        return formatted_title_text

    def get_body(self, soup):
        """
        Gets the body of a post from a soup object
        :param soup: the soup of a post
        :return: the body of the post
        """

        body_text_class = "usertext-body may-blank-within md-container"
        all_text_div = soup.find_all("div", class_=body_text_class)

        if len(all_text_div) >= 2:
            page_body = all_text_div[1]
        else:
            raise ValueError("The get_body() function should find 100+ text_divs with the specified classes. "
                             "This function is probably called with the wrong soup.")
        return page_body.get_text().strip()

    def get_comments(self, post_list):
        """
        Gets "relevant" comments from a list of posts
        :param post_list: a list of posts
        :return: list of relevant comments
        """

        comment_text_list = []

        self.get_page_data(post_list[0])
        return comment_text_list

    def get_post_data(self, post_list):
        """
        Gets the data from each post in a list of posts
        :param post_list: list of links to posts
        :return: dictionary with the post title as a key and the post body as the value
        """

        post_dictionary = {}
        for post_link in post_list:
            webpage_html = self.get_page_data(post_link)
            post_soup = self.create_soup(webpage_html)

            post_title = self.get_title(post_soup)
            post_body = self.get_body(post_soup)

            post_dictionary[post_title] = post_body
            print(len(post_dictionary))
        return post_dictionary

    def save_posts(self, post_dictionary, save_file):
        """
        Neatly writes the posts to a file
        :param post_dictionary: dictionary of posts, title:body
        :param save_file: file to write posts to
        """

        with open(save_file, 'w', encoding='utf-8') as writer:
            for title in post_dictionary:
                body = post_dictionary[title]

                writer.write(title + "\n")
                writer.write(body + "\n\n")


if __name__ == "__main__":
    url_access = "https://old.reddit.com/r/AmItheAsshole/"
    main_file = "web_page.html"
    comment_file = "comment_save.html"
    post_save_file = "temp_text.txt"

    parser = Parser()

    # Uncomment below to save new set of posts
    # parser.get_page_data_file(url_access, main_file)
    page = parser.create_soup_file(main_file)

    # Gets a list of posts for
    post_links_list = parser.get_post_links(page)
    # Saves post data to a file
    parser.save_posts(parser.get_post_data(post_links_list), post_save_file)

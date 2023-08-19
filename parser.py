import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen

"""
Manages html data
"""


class Parser:

    def get_page_data_file(self, url, filename):
        """
        Writes a webpages html to a file
        @param url: the url of the page to access
        @param filename: the file to write the html to
        """

        webpage = urlopen(url).read()
        with open(filename, "wb") as writer:
            writer.write(webpage)


    def get_page_data(self, url):
        """
        
        @param url:
        @return:
        """

        return urlopen(url).read()

    def create_soup_file(self, filename):
        """
        Creates a BeautifulSoup object from a file
        @param filename: the file to create soup from
        @return: BeautifulSoup object
        """

        with open(filename, "rb") as reader:
            return BeautifulSoup(reader, "html.parser")

    def create_soup(self, webpage):
        """
        Creates a BeautifulSoup object from a webpage
        @param webpage: the page to create soup from
        @return: BeautifulSoup object
        """

        return BeautifulSoup(webpage, "html.parser")


    def get_post_links(self, soup):
        """
        Gets the links of all posts
        @param soup: soup object to parse
        @return: list of all post links on page
        """

        posts = []
        for link in soup.find_all('a'):
            link = link.get('href')
            if "/comments/" in link and link not in posts:
                posts.append(link)
        return ["https://www.reddit.com" + post for post in posts]


    def get_post_data(self, post_list):
        """
        Gets the data from each post in a list of posts
        :param post_list: list of links to posts
        :return: dictionary with the post title as a key and the post body as the value
        """

        post_dictionary = {}
        for post_link in post_list:
            webpage_html = self.get_page_data(post_list)
            post_soup = self.create_soup(webpage_html)

            post_title = self.get_title(post_soup)
            post_body = self.get_body(post_soup)

            post_dictionary[post_title] = post_body
        return post_dictionary

    def get_title(self, soup):
        return None

    def get_body(self, soup):
        return None

    def get_comments(self, post_list, filename):
        comment_text_list = []

        self.get_page_data(post_list[0], filename)
        '''
        for comment_url in comment_list:
            self.get_page_data(comment_url, filename)
            comment_page = self.create_soup(filename)

            comment_text = comment_page.find_all(attrs={"data-testid": "comment"})
            comment_text_list.append(comment_text)
        '''
        return comment_text_list


if __name__ == "__main__":
    url_access = "https://www.reddit.com/r/AmItheAsshole/"
    main_file = "web_page.html"
    comment_file = "comment_save.html"

    parser = Parser()
    parser.get_page_data_file(url_access, main_file)
    page = parser.create_soup_file(main_file)

    titles = parser.get_post_links(page)
    #print(parser.get_comments(titles, comment_file))

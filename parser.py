import time
from bs4 import BeautifulSoup
from urllib.request import urlopen

"""
Manages html data
"""


class Parser:

    def get_page_data_file(self, url, filename):
        """
        Writes a webpage's html to a file
        :param url: the url of the page to access
        :param filename: the file to write the html to
        """

        webpage = urlopen(url, timeout=10).read()
        with open(filename, "wb") as writer:
            writer.write(webpage)

    def get_page_data(self, url):
        """
        Returns the html data from a page
        :param url: the url of the page to access
        :return: html data of the url
        """

        return urlopen(url, timeout=100).read()

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

        return posts[num_pinned_posts:]

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
        '''
        for comment_url in comment_list:
            self.get_page_data(comment_url, filename)
            comment_page = self.create_soup(filename)

            comment_text = comment_page.find_all(attrs={"data-testid": "comment"})
            comment_text_list.append(comment_text)
        '''
        return comment_text_list

    def get_post_data(self, post_list):
        """
        Gets the data from each post in a list of posts
        :param post_list: list of links to posts
        :return: dictionary with the post title as a key and the post body as the value
        """

        post_dictionary = {}
        x = 0
        for post_link in post_list:
            webpage_html = self.get_page_data(post_link)
            post_soup = self.create_soup(webpage_html)

            post_title = self.get_title(post_soup)
            post_body = self.get_body(post_soup)

            post_dictionary[post_title] = post_body
            x += 1
            print(x)
        return post_dictionary

    def write_dic(self, dict):
        with open("temp_text.txt", 'w') as writer:
            for key in dict:
                writer.write(key)
                writer.write(dict[key])


if __name__ == "__main__":
    url_access = "https://old.reddit.com/r/AmItheAsshole/"
    main_file = "web_page.html"
    comment_file = "comment_save.html"

    parser = Parser()
    # parser.get_page_data_file(url_access, main_file)
    page = parser.create_soup_file(main_file)

    post_links_array = parser.get_post_links(page)
    # print(post_links_array)
    # test_page_data = parser.get_page_data(titles[3])
    # test_page_soup = parser.create_soup(test_page_data)
    parser.write_dic(parser.get_post_data(post_links_array))


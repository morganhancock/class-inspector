import sys
import os
from bs4 import BeautifulSoup

proj_path = sys.argv[1]

APPROVED_TAGS = ['Topics', 'Sections', 'HomePage', 'Training', 'Search']
DEFAULT_HTML_TAG = ['Topics']
DEFAULT_IMG_CLASS = ['']


class Report:
    absolute_path = r'C:\...'


class TestResult:
    pass_fail = False



def warning():
    """Issues a warning and returns True or False based on user input"""
    print('This will write to disk and you could mess stuff up.')
    answer = input('Are you sure Y/N?: ')
    if answer == 'y' or answer == 'Y':
        result = True
    else:
        result = False
    return result


def get_contents(path):
    """Takes a path and returns all .htm content files within."""
    # init null lists to be filled in
    files_to_check = []
    file_list = []
    # get all files (not directories) within path, append to files_to_check
    for root, directories, filenames in os.walk(path):
        for filename in filenames:
            files_to_check.append(os.path.join(root, filename))
            # iterate over files_to_check, if .htm file, add to file_list
    for file in files_to_check:
        root, filename = os.path.split(file)
        if os.path.splitext(filename)[1] == '.htm':
            file_list.append(os.path.join(root, filename))
    return file_list


def make_soup(file):
    contents = open(file, encoding='utf-8-sig').read()
    soup = BeautifulSoup(contents, 'html.parser')
    return soup


def test_images(soup, file, message):
    if file != "home.htm":
        for tag in soup.find_all('img'):
            if tag.parent.name == 'figure':
                tag.parent.wrap(soup.new_tag("div"))
                del tag['style']
                del tag['class']
                tag['class'] = ['img-responsive center-block']
                print(soup)

def test_a_element(soup, file, message):
    for tag in soup.find_all('a'):
        name = tag.get('name')
        href = tag.get('href')
        if name and not href:
            tag['class'] = ['anchor']
            print(tag)




def test_class(soup, file, message):
    for tag in soup.find_all('html'):
        # REMEMBER: normally you can just define a single word for an
        # attribute, but class is a special flower that requires a list,
        # even if that list is only one element long.
        html_class = tag.get('class')
        if not html_class:
            message += '\nNo class tag in html element of file {0}'.format(file)
            message += '\nDefault class tag "{0}" was added'.format(DEFAULT_HTML_TAG)
            message += '\n' + '#'*100
            tag['class'] = DEFAULT_HTML_TAG
        else:
            if len(html_class) > 1:
                new_tag = []
                for subclass in tag['class']:
                    if subclass in APPROVED_TAGS:
                        if len(new_tag) > 0:
                            message += '\nMultiple approved class tags "{0}" found in html element of file {1}'.format(html_class, file)
                            message += '\nNO CHANGES WERE MADE'
                            message += '\n' + '#'*100
                            break
                        else:
                            new_tag.append(subclass)
                if not new_tag:
                    message += '\nMultiple non-approved class tags "{0}" found in html element of file {1}'.format(html_class, file)
                    message += '\n' + '#'*100
                    tag['class'] = new_tag
            elif html_class[0] not in APPROVED_TAGS:
                message += '\nNon-approved class tag "{0}" found in html element of file {1}'.format(html_class[0], file)
                message += '\n' + '#'*100
                tag['class'] = DEFAULT_HTML_TAG

    print(message)

    # print(file)
    # with open(file, 'w', encoding='utf-8-sig') as o:
    #	o.write(str(soup))

def main():
    if warning():
        message = ''
        for file in get_contents(proj_path):
            soup = make_soup(file)
            #test_images(soup, file, message)
            # test_class(file, message)
            test_a_element(soup, file, message)

        print(message)

    # print(file)
    # with open(file, 'w', encoding='utf-8-sig') as o:
    #	o.write(str(soup))


main()

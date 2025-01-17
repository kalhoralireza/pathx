from urllib.parse import urlparse
import argparse
import sys

def append_string_to_path(url, string):
    parsed_url = urlparse(url)
    if parsed_url.path[-1] != '/':
        path = parsed_url.path + '/'    
    else:
        path = parsed_url.path
    
    path_segments = path.split('/')
    result_urls = set()
    for i in range(2, len(path_segments)+1):
        if i == len(path_segments):
            new_path = '/'.join(path_segments[:i]) + string 
        else:
            new_path = '/'.join(path_segments[:i]) + string + '/' + '/'.join(path_segments[i:])

        if parsed_url.query != '':
            new_url = parsed_url.scheme + '://' + parsed_url.netloc + new_path + '?' + parsed_url.query
        else:
            new_url = parsed_url.scheme + '://' + parsed_url.netloc + new_path
        
        result_urls.add(new_url)
    
    for i in range(1, len(path_segments)+1):
        if i == len(path_segments):
            new_path = '/'.join(path_segments[:i]) + string 
        else:
            new_path = '/'.join(path_segments[:i]) + '/' + string + '/' + '/'.join(path_segments[i:]) 
        
        if parsed_url.query != '':
            new_url = parsed_url.scheme + '://' + parsed_url.netloc + new_path + '?' + parsed_url.query
        else:
            new_url = parsed_url.scheme + '://' + parsed_url.netloc + new_path 
        
        result_urls.add(new_url) 
        
    return result_urls



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Appending string in different ways to a URL path.')
    parser.add_argument('-l', '--list', type=str, help='target URL file.')
    parser.add_argument('-s', '--string', type=str, help='string to append to the URL path.')
    args = parser.parse_args()

    if sys.stdin.isatty():
        if not args.list or not args.string:
            print('Please provide both a URL and string to append to the path.')
        else:
            with open(args.list) as input_file:
                for url in input_file.readlines():
                    result_urls = append_string_to_path(url.rstrip(), args.string)
                    for url in result_urls:
                        print(url)
    else:
        for line in sys.stdin:
            url = line.strip()
            result_urls = append_string_to_path(url, args.string)
            for new_url in result_urls:
                print(new_url)

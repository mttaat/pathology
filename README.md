# pathology
A web path fuzzer in the spirit of dirbuster with support for multiple concurrent domains, arbitrary file extensions and user-definable success/failure criteria based on response page text.

Historically attackers were able to find path traversals and hidden directories on webservers by utilizing a large wordlist, concatenating each entry to the target domain and reading the response code returned by the request. 200 signified a possibly new juicy target directory and 404 or other errors signified a miss. Modern web servers and web applications tend to return 200 for many requests which would otherwise fail, and the paths used by their pages do not neccessarily reflect an actual directory on the web server but a software-defined route to a method or other non-file resource. 

This project aims to provide a flexible script to aid in "fuzzing" the path aspect of modern web apps, specifically by (mostly) ignoring the server-returned HTTP code and instead parsing the returned *content* for a set of user-defined pass/fail regex. Example regex may be of the form:


**Example invocations:**

    python pathology.py -t 'aol.com,yahoo.com,compuserve.com' -l ./directory-list-lowercase-2.3-small.txt -m 'GET,HEAD,OPTIONS'
    python pathology.py -t ./domains.txt -l 'admin,console,passwords,users,customers,clients,business -m 'GET,DELETE'

Both are optional and if neither is passed by the user then pathology will fall back onto HTTP response codes (404, 200, 500, etc)

Pathology also supports targeting of multiple domains and may read this input from a file. Scan results may be output to stdout or to a filename.

Inspiration from OWASP's dirbuster and NoobieDog's Dir-Xcan - https://github.com/NoobieDog/Dir-Xcan


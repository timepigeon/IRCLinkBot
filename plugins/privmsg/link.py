from __future__ import unicode_literals
def main(data):
    from HTMLParser import HTMLParser
    args = argv('@',data['recv'])
    # look for URL
    link = geturl(data['recv'])
    if link and link != "" and not modeCheck('b', data):
        parser = HTMLParser()
        link = link[0]
        # look for title
        badext = ('.cgi','.pdf')
        imgext = ('.jpg','.png','.gif','.bmp')
        if not link[-4:].lower() in badext:
            if not link[-4:].lower() in imgext:
                title = gettitle(link)
                if title:
                    # encode unicode object to byte string
                    # if type(title) == unicode:
                        # title = title.encode('utf-8', "ignore")
                    title = unicode(title)
                    title = parser.unescape(title)
                    title = title.replace('\n',' ')
                    title = title.replace('\r',' ')
                    title = title.strip()
                    if len(title) >= 150:
                        title = title[:150]
                    if len(link) > int(data['config']['settings']['maxLinkLen']):
                        # post title + tiny
                        data['api'].say(args['channel'], '^ ' + title + ' ' + maketiny(link) + ' ^')
                        return
                    else:
                        # post title only
                        data['api'].say(args['channel'], '^ ' + title + ' ^')
                        return
            else:
                # We've got an image URL.
                from alchemyapi import AlchemyAPI
                alchemyapi = AlchemyAPI()
                response = alchemyapi.imageTagging('url', link)
                if response['status'] == 'OK' and response['imageKeywords'][0]['text'] != 'NO_TAGS':
                    retme = "^ Image of: "
                    for keyword in response['imageKeywords']:
                        retme += "%s(%s%%) " % (keyword['text'], int(float(keyword['score']) * 100))
                    if len(link) > int(data['config']['settings']['maxLinkLen']):
                        retme += maketiny(link) + " "
                    retme += "^"
                    data['api'].say(args['channel'], retme)
                    return
        if len(link) > int(data['config']['settings']['maxLinkLen']):
            # post tiny only
            data['api'].say(args['channel'], '^ ' + maketiny(link) + ' ^')
            return
        else:
            # nothing
            return False

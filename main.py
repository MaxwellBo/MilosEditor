import praw
import re

CLIENT_ID="?"
CLIENT_SECRET="?"
USER_AGENT="?"

reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT
)

incantation = re.compile(r"!milos-editor A(\d+)")

def make_reply(annotation_code):
    image = f"[Comment \[A[{annotation_code}\]](https://i.imgur.com/{annotation_code})" 
    horizontal_rule = "???"
    bot_maintainer_contact = "???" # TODO: make small and subscripted

    return "\n".join([image, horizontal_rule, bot_maintainer_contact])

def process(comment):
    match = incantation.match(comment.body)
    
    if match:
        annotation_code = int(match.group(1)) # groups in matches are 1-indexed
        comment.reply(make_reply(annotation_code))

while True:    
    for c in r.get_all_comments(limit = None, url_data = {'limit':100} ):

        try:
            process(c)
        except KeyboardInterrupt:
            exit(0)
        except praw.errors.APIException, e:
            print("[ERROR]:", e)
            sleep(30)                
        except Exception, e:
            print("[ERROR]:", e)
            continue

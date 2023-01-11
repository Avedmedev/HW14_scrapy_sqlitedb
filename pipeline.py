import logging
from datetime import datetime

from sqlalchemy.exc import IntegrityError

from models import Session, Author, Quote, Tag
from itemadapter import ItemAdapter


class SpiderPipeLine(object):

    session = Session()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if 'author' in adapter.keys():
            if not self.session.query(Quote).filter(Quote.content == adapter['quote']).first():
                author = self.session.query(Author).filter(Author.fullname == adapter['author']).first()
                if not author:
                    author = Author(fullname=adapter['author'])
                    self.session.add(author)
                    self.session.commit()
                    author = self.session.query(Author).filter(Author.fullname == adapter['author']).first()

                tags_obj = []
                for new_tag in adapter['tags']:
                    tag = self.session.query(Tag).filter(Tag.tagname == new_tag).first()
                    if not tag:
                        tag = Tag(tagname=new_tag)
                        self.session.add(tag)
                        self.session.commit()
                        tag = self.session.query(Tag).filter(Tag.tagname == new_tag).first()
                    tags_obj.append(tag)

                quote = Quote(content=adapter['quote'], tags=tags_obj, author=author)
                self.session.add(quote)
                self.session.commit()

        if 'fullname' in adapter.keys():
            author = self.session.query(Author).filter(Author.fullname == adapter['fullname']).first()
            if not author:
                author = Author(fullname=adapter['fullname'],
                                born_date=datetime.strptime(adapter['born_date'], "%B %d, %Y").isoformat(),
                                born_location=adapter['born_location'],
                                bio=adapter['bio']
                                )
                self.session.add(author)
                self.session.commit()
            else:
                author.born_date = datetime.strptime(adapter['born_date'], "%B %d, %Y").isoformat()
                author.born_location = adapter['born_location']
                author.bio = adapter['bio']
                self.session.commit()

    def close_spider(self, spider):
        self.session.close()


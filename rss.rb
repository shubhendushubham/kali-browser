require 'rss'
require 'open-uri'

module Jekyll
  class RSSFetcher < Generator
    safe true

    def generate(site)
      feed_urls = [
        'https://example.com/rss1',
        'https://example.com/rss2',
        'https://example.com/rss3'
      ]

      all_articles = []

      feed_urls.each do |feed_url|
        rss_content = URI.open(feed_url).read
        rss = RSS::Parser.parse(rss_content, false)

        articles = rss.items.map do |item|
          {
            'title' => item.title,
            'link' => item.link,
            'description' => item.description,
            'pubDate' => item.pubDate,
            'source' => feed_url
          }
        end

        all_articles.concat(articles)
      end

      site.data['news'] = all_articles
    end
  end
end

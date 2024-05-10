require 'watir'
require 'uri'

# Check if a search parameter is provided as a command-line argument
if ARGV.empty?
  puts "Usage: ruby script.rb <search_parameter>"
  exit 1
end

# Retrieve the search parameter from the command-line arguments
search_parameter = ARGV.join(' ')

# Google search query for PDF files using the Google dork with the parameter in the URL
query = "inurl:.pdf #{search_parameter}"

# Perform Google search
browser = Watir::Browser.new :chrome
browser.goto("https://www.google.com/search?q=#{URI.encode_www_form_component(query)}")

# Wait for the search results to load
sleep 5

# Extract search results URLs
pdf_links = browser.links(href: /\.pdf$/)

# Print PDF links
pdf_links.each do |link|
  puts "PDF URL: #{link.href}"
end

# Wait for 2 minutes (120 seconds)
sleep 120

# Close the browser
browser.close

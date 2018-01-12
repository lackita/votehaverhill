require "httparty"
require "pp"

results = HTTParty.get("https://www.googleapis.com/civicinfo/v2/divisions?key=#{ENV['VOTE_HAVERHILL_API_KEY']}&query=Haverhill")

divisions = results["results"].select { |result| result["ocdId"] =~ /^ocd-division\/country:us\/state:ma\/place:haverhill/ }
pp divisions

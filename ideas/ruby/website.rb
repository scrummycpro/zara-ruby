# Run the Python script
system("python3 test.py")

require 'optparse'

o = {}
OptionParser.new { |p| o[:ls] = true }.parse!
c = nil

# Function to print a big bold title
def print_title(title)
  puts "\e[1m#{title}\e[0m"  # Bold text
end

loop do
  print_title("COMMANDS")

  puts "Select a command:"
  puts "1. \e[32mList files\e[0m"      # Green color
  puts "2. \e[34mOpen Vim\e[0m"        # Blue color
  puts "3. \e[35mOpen Visual Studio Code\e[0m"  # Magenta color

  print "Enter your choice: "
  c = gets.chomp.to_i

  break if (1..3).include?(c)
  puts "\e[31mInvalid choice. Please try again.\e[0m"  # Red color
end

exec(c == 1 && o[:ls] ? "ls" : c == 2 ? "vim" : c == 3 ? "code" : "")

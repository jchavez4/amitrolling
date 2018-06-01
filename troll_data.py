import calendar

#could do timeline of tweets
#do timeline of creation of accounts
#most frequent words found in the russian troll tweets in general
    #most frequent words before election
    #most frequent words after election


def parse_account_data(dates):
    only_months = []

    for date in dates:
        tmp = []
        if date[0]:
            separated = date[0].split()
            tmp.append(separated[-1])
            #get numerical month from str abbreviation
            month = list(calendar.month_abbr).index(separated[1])
            tmp.append(month)
            only_months.append(tmp)

    return only_months


def count_per_month(only_months):
    years = {}

    #create double dictionary to get counts per year per month of tweets
    for date in only_months:
        years[int(date[0])] = years.get(int(date[0]), {})

        month_dict = years.get(int(date[0]))

        month_dict[int(date[1])] = month_dict.get(int(date[1]), 0) + 1

    #create list of counts per month per year to send
    month_counts = []
    for key, value in sorted(years.items()):
        if key == 2016 or key == 2017:
            counts = []
            for month, count in sorted(years.get(key).items()):
                counts.append(count)
            month_counts.append(counts)

    return month_counts

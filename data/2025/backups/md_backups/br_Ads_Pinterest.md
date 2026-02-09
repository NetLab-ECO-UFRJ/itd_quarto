## SPECIAL CRITERIA

**SC1: Does the platform provide an API to access its ad repository and
extract data on advertising content?** - weight 0.50

This item verifies whether the platform provides an ad repository API
with at least one endpoint for programmatically extracting advertising
data. Full availability is confirmed when the API returns information on
ads across all categories. The assessment should confirm that the
endpoint allows the retrieval and storage of ad data without requiring
privileged or internal access beyond standard developer registration.

  - > Yes, with full availability

  - > Yes, with partial availability

  - > **No**

**Justification:**

Although Pinterest maintains a public Ads Repository, it does not make
this data available through an Ads Repository API.
[<span class="underline">Previous versions of the Pinterest
API</span>](https://assets.mofoprod.net/network/documents/Full_Disclosure_Stress_Testing_Tech_Platforms_Ad_Repositories_3FepU2u.pdf),
deprecated as of 2022, included endpoints for accessing advertising
data, but this capability is not present in the current
[<span class="underline">Pinterest API
v5</span>](https://developers.pinterest.com/docs/api/v5/introduction/?).

**SC2: Does the platform provide a graphical user interface to its ad
repository for extracting advertising content data?** - weight 0.30

This item verifies whether the platform provides a graphical user
interface (GUI) for extracting ad data in a structured format for
external use. Full availability is considered granted when the GUI
delivers information on ads across all categories. The assessment should
confirm the availability of an official browser-based tool that allows
users not only to view ad content but also to export its data.

  - > Yes, with full availability

  - > Yes, with partial availability

  - > **No**

**Justification:**

Although Pinterest maintains a public Ads Repository, it does not allow
data to be extracted in a structured format, limiting access to viewing
ad content only.

**SC3: Can data from both active and inactive ads be extracted?** -
weight 0.20

This item verifies whether the platform allows the extraction of ad data
through either the GUI or the API, from at least one day after
publication to at least one year prior. Full availability is confirmed
when both active and inactive ad data are delivered across all ad
categories. The assessment should test the interface and endpoints to
confirm whether both active and inactive ads can be retrieved.

  - > Yes, with full availability

  - > Yes, with partial availability

  - > **No**

**Justification:**

Although Pinterest maintains a public Ads Repository, it does not allow
data to be extracted in a structured format, either through its
graphical user interface or via an API, limiting access to viewing ad
content only.

## OTHER CRITERIA

### ACCESSIBILITY

*Accessibility measures how easily data can be located, retrieved,
understood and used.*

**OC1: Does the platform provide a GUI for accessing and visualizing its
ad repository?\***

This item verifies whether the platform provides a GUI for accessing and
viewing ads in its ad repository. Full access is confirmed when the GUI
provides information on ads across all categories and publication
statuses, including both active and inactive ads. The assessment should
confirm the availability of an official browser-based tool that allows
users to search, access, and view ad content.

  - > **Yes, with full availability**

  - > Yes, with partial availability

  - > No

**Justification:**

The [<span class="underline">Pinterest Ads
Repository</span>](https://ads.pinterest.com/ads-repository/) publicly
provides, through its GUI, all ads served to users in Brazil in the last
year, both active and inactive.

**OC2: Is access to the platform’s ad repository free of charge?**

This item verifies whether the ad repository API or GUI is free of
charge, since even modest fees can create barriers or force researchers
in low-resourced settings to narrow the scope of their work. The
assessment should verify the platform’s documentation and pricing
policies to confirm that no fees are applied for access to the ad
repository.

  - Free API access

  - **Free GUI access**

  - No

**Justification:**

The Pinterest Ads Repository is freely accessible, but no API exists,
and access is limited to its GUI.

**OC3: Can the requested data be extracted directly from the ad
repository response?**

This item verifies whether the platform’s ad repository returns
structured data on ad content and authorship directly in the response,
rather than providing a link that redirects to the data. Audiovisual
media files and data (e.g., images, videos, and audio) should not be
considered when assessing this item. The assessment should examine
sample data responses from both the ad repository GUI and API to confirm
that the requested public data is included in the returned payload.

  - > Yes, through the GUI

  - > Yes, through the API

  - > **No**

**Justification:**

The Pinterest Ads Repository does not allow the extraction of structured
data.

**OC4: Does the platform’s ad repository API provide a form of
authentication that allows for renewal without the risk of data
loss?\***

This item verifies whether the tokens provided for API use can be
renewed without the risk of data loss, ensuring continuity and integrity
of data access and monitoring. The assessment should check the
platform’s documentation or directly observe the authentication and
renewal process to confirm that token updates do not interrupt or
compromise data access.

  - > Yes

  - > **No**

**Justification:**

The Pinterest Ads Repository offers no API access under any
circumstances.

**OC5: Can data from an individual ad be retrieved from the platform?**

This item verifies whether it is possible to retrieve data from a
specific advertisement on the ad repository using a unique identifier,
rather than relying on search terms or other parameters and filters. The
assessment should review the ad repository documentation and test
available features to confirm that an individual ad can be retrieved
directly by its unique identifier.

  - > **Yes, through the GUI**

  - > Yes, through the API

  - > No

**Justification:**

The Pinterest Ads Repository allows users to retrieve specific ads by
their ID through the GUI.

**OC6: Can data from ads served by a specific advertiser be retrieved
from the platform?**

This item verifies whether it is possible to retrieve data from ads run
by a specific advertiser, via their username or unique identifier. The
assessment should review the ad repository documentation and test any
available feature to retrieve data from an individual advertiser.

  - > **Yes, through the GUI**

  - > Yes, through the API

  - > No

**Justification:**

The Pinterest Ads Repository allows users to retrieve ads by selecting
specific advertisers.

**OC7: Can ad data be retrieved from the platform using search terms?**

This item verifies whether ad data can be retrieved through search
terms, enabling the creation of datasets based on those queries. The
assessment should test search-related features to confirm that it
accepts search queries using keywords.

  - > Yes, through the GUI

  - > Yes, through the API

  - > **No**

**Justification:**

The Pinterest Ads Repository does not allow ads to be retrieved using
search terms.

**OC8: Does the platform use locale-neutral data representations?**

This item verifies whether locale-sensitive data (e.g., timestamps,
currency, numbers) are provided in a locale-neutral format, or, if that
is not possible, whether relevant locale metadata is included. The
assessment should review the ad repository documentation and inspect
sample responses to confirm the presence of standardized formats or
accompanying metadata.

  - > **Yes, through the GUI**

  - > Yes, through the API

  - > No

**Justification:**

The Pinterest Ads Repository GUI displays dates in ISO 8601 format
(YYYY-MM-DD).

### COMPLETENESS

*Completeness refers to how closely the data reflects the dimensions of
what it represents (in breadth, depth and scope).*

**OC9: Does the platform provide data that allows the identification of
advertisers who ran ads?**

This item verifies whether the platform discloses information on the
advertisers responsible for the identified ads. The assessment should
confirm whether the advertiser’s page name, URL, and unique identifier
can be retrieved.

  - > **Yes, through the GUI**

  - > Yes, through the API

  - > No

**Justification:**

Advertiser identities are accurately disclosed in the Pinterest Ads
Repository.

**OC10: Does the platform provide data on the funders who paid for
ads?**

This item verifies whether the platform provides data on the individuals
or organizations that paid for the identified ads. The assessment should
confirm whether any sponsor information is retrievable.

  - > Yes, through the GUI

  - > Yes, through the API

  - > **No**

**Justification:**

The Pinterest Ads Repository does not disclose who paid for ads served
on the platform.

**OC11: Does the platform provide data on the period during which ads
were served?**

This item verifies whether the platform provides data on the days on
which the identified ads ran. The assessment should review the extracted
ad data to confirm that it includes start and end dates (or equivalent
temporal markers) indicating the period of activity.

  - > **Yes, through the GUI**

  - > Yes, through the API

  - > No

**Justification:**

The Pinterest Ads Repository discloses the start and end dates of ad
delivery to users on the platform.

**OC12: Does the platform provide data on user engagement with ads?**

This item verifies whether the platform provides data on the total
number of user interactions with ads (e.g., likes, comments, shares,
clicks). The assessment should review the extracted ad data to confirm
that engagement metrics are available and clearly linked to each ad.

  - > Yes, through the GUI

  - > Yes, through the API

  - > **No**

**Justification:**

The Pinterest Ads Repository does not provide any data on user
engagement with ads.

**OC13: Does the platform indicate whether ads were placed by verified
or unverified advertisers?**

This item verifies whether the platform clearly indicates whether
advertisers were verified at the time their ads were served. The
assessment should review ad records to confirm that a verification
status field is present.

  - > Yes, through the GUI

  - > Yes, through the API

  - > **No**

**Justification:**

The Pinterest Ads Repository does not disclose any information on
advertisers’ verification status.

### COMPLIANCE

*Compliance refers to how data adheres to standards, conventions and
regulations in a given context. It ensures that data is formatted and
structured in the way it ought to be, according to external or internal
rules.*

**OC14: Does the platform flag ads that were removed due to violations
of its guidelines or relevant legislation?**

This item verifies whether the platform indicates when an ad has been
moderated. At a minimum, the platform should provide the reason for
removal and the date. The assessment should review ad records to confirm
that moderated ads are flagged and that the corresponding moderation
details are clearly documented.

  - > Yes, through the GUI

  - > Yes, through the API

  - > **No**

**Justification:**

We did not identify any ads flagged as removed or moderated during our
testing of the Pinterest Ads Repository.

**OC15: Does the platform indicate whether ad content was generated
using artificial intelligence?**

This item verifies whether the platform flags ads in which AI was
involved in generating the content. The assessment should review ad
records to confirm the presence of a field or label indicating the use
of AI in ad production.

  - > Yes, through the GUI

  - > Yes, through the API

  - > **No**

**Justification:**

The Pinterest Ads Repository does not provide any information regarding
the use of generative AI in the creation or manipulation of ad content.

**OC16: Is the platform’s ad repository documentation published in open
access?**

This item verifies whether the platform makes its ad repository
documentation openly available on the internet, without requiring user
registration or login. The assessment should attempt to access the
documentation directly to confirm that it is fully available without
authentication barriers.

  - > Yes, the API documentation

  - > Yes, the GUI documentation

  - > **No**

**Justification:**

No documentation for the Pinterest Ads Repository could be identified.
The repository’s GUI only references a [<span class="underline">broken
link</span>](https://developers.pinterest.com/docs/api/v4/#tag/ads_repository)
that previously directed users to deprecated versions of the Pinterest
API, which included endpoints for collecting ad data.

**OC17: Is the platform’s ad repository documentation clearly written
and exemplified?**

This item verifies whether the documentation for the platform’s ad
repository is clear, complete, and provides practical implementation
examples. The assessment should review the documentation to confirm the
presence of detailed explanations, structured references, and sample
queries or outputs illustrating correct use.

  - > Yes, the API documentation

  - > Yes, the GUI documentation

  - > **No**

**Justification:**

No documentation for the Pinterest Ads Repository could be identified.
The repository’s GUI only references a [<span class="underline">broken
link</span>](https://developers.pinterest.com/docs/api/v4/#tag/ads_repository)
that previously directed users to deprecated versions of the Pinterest
API, which included endpoints for collecting ad data.

**OC18: Does the platform’s ad repository documentation include or link
to its terms of use?**

This item verifies whether the documentation clearly and unambiguously
states or refers to the terms for using the ad repository and its
associated legal aspects. The assessment should review the documentation
to confirm that explicit terms or references are provided and
accessible.

  - > Yes, the API documentation

  - > Yes, the GUI documentation

  - > **No**

**Justification:**

No documentation for the Pinterest Ads Repository could be identified.
The repository’s GUI only references a [<span class="underline">broken
link</span>](https://developers.pinterest.com/docs/api/v4/#tag/ads_repository)
that previously directed users to deprecated versions of the Pinterest
API, which included endpoints for collecting ad data.

**OC19: Does the platform provide its ad repository documentation in the
official languages of the assessed region?**

This item verifies whether the platform provides its ad repository
documentation in the official languages of the region being assessed.
The assessment should review the documentation to confirm that complete
and up-to-date versions are available in those languages.

  - > Yes, the API documentation

  - > Yes, the GUI documentation

  - > **No**

**Justification:**

No documentation for the Pinterest Ads Repository could be identified.
The repository’s GUI only references a [<span class="underline">broken
link</span>](https://developers.pinterest.com/docs/api/v4/#tag/ads_repository)
that previously directed users to deprecated versions of the Pinterest
API, which included endpoints for collecting ad data.

**OC20: Does the platform implement a proper deprecation strategy to
avoid breaking client applications while rolling out major changes in
the API?\***

This item verifies whether the platform’s documentation describes a
deprecation strategy with a grace period before removing features. The
assessment should review changelogs to confirm that deprecated features
are listed with deprecation and removal dates and include migration
instructions. This item applies only to breaking changes that require
client updates, such as endpoint modifications, authentication updates,
or the removal of features.

  - > Yes

  - > **No or not applicable**

**Justification:**

The Pinterest Ads Repository offers no API access under any
circumstances.

**OC21: Does the platform’s ad repository API documentation detail the
response format of each endpoint?\***

This item verifies whether the platform’s ad repository API
documentation specifies the format of each possible response, including
examples and potential errors. The assessment should review the
documentation to confirm that response structures are described and
illustrated with sample outputs.

  - > Yes

  - > **No or not applicable**

**Justification:**

The Pinterest Ads Repository offers no API access under any
circumstances.

**OC22: Does the platform’s ad repository API documentation detail the
quota or rate limits applicable to each available endpoint?\***

This item verifies whether the platform’s ad repository API
documentation specifies the limits for each endpoint, including any
variations based on authentication level or endpoint type. Rate and
quota limits define the maximum number of requests allowed within a
given period (e.g., 1,000 requests per hour). The assessment should
review the documentation to confirm that request caps (rate limits) and
overall usage restrictions (quotas) are clearly stated.

  - > Yes

  - > **No or not applicable**

**Justification:**

The Pinterest Ads Repository offers no API access under any
circumstances.

### CONSISTENCY

*This dimension tracks whether the data always presents the same values,
the same format in every occurrence and if it is compatible with the
previous data.*

**OC23: Does the data retrieved by the API reflect what is displayed on
the platform’s ad repository GUI?\***

This item verifies whether the data returned by the platform’s ad
repository API corresponds to the information displayed on its GUI in
all its levels of detail. It should be possible to identify in the API
response information such as authorship, complete content, and other
serving information (e.g., amount spent, impressions reached). The
assessment should compare API responses with the GUI to confirm that at
least the following elements are consistent: authorship, full content,
and serving information (e.g., spending, impressions).

  - > Yes

  - > **No or not applicable**

**Justification:**

The Pinterest Ads Repository offers no API access under any
circumstances.

**OC24: Are the results returned by the platform consistently
reproducible?**

This item verifies whether data accessed and extracted via the
platform’s ad repository at a given time is consistent with other
collections performed similarly, including cases where content was
deleted in the interim. The assessment should perform repeated queries
to confirm the reproducibility of results.

  - > **Yes, through the GUI**

  - > Yes, through the API

  - > No

**Justification:**

The Pinterest Ads Repository GUI was found to return consistent results
across repeated queries.

**OC25: Is the data returned by the platform consistent with the
parameters and filters used in the request?**

This item verifies whether the data retrieved through the ad repository
accurately reflects the parameters and filters specified at the time of
the request. The assessment should run test queries with different
filters to confirm that results consistently match the requested
conditions.

  - > **Yes, through the GUI**

  - > Yes, through the API

  - > No

**Justification:**

Results obtained from the Pinterest Ads Repository were consistent with
the filters and parameters defined throughout the testing process.

### RELEVANCE

*Relevance evaluates how helpful the data is and how applicable for use
it is, also considering future applications. This dimension also
evaluates the extent to which the content and coverage of data meet the
user’s needs.*

**OC26: Does the platform allow the use of temporal filters to retrieve
data on ads?**

This item verifies whether the ad repository allows filtering data by
the time period in which the ads were served. The assessment should test
queries with temporal filters to confirm that results accurately reflect
the specified date ranges.

  - > **Yes, through the GUI**

  - > Yes, through the API

  - > No

**Justification:**

The Pinterest Ads Repository allows users to filter results by
specifying ad delivery start and end dates. However, the maximum
allowable interval between these dates is 30 days, which substantially
limits research and inquiry capabilities.

**OC27: Does the platform allow filtering advertising data by ad
category?**

This item verifies whether the ad repository allows filtering data by
any categories assigned at the time of ad creation. The assessment
should run test queries with category filters to confirm that results
align with the selected classifications.

  - > **Yes, through the GUI**

  - > Yes, through the API

  - > No or not applicable

**Justification:**

The Pinterest Ads Repository allows users to filter results by thematic
categories, including “Animals”, “Architecture”, “Arts”, “Health”, and
others.

**OC28: Does the platform allow filtering advertising data by geographic
location?**

This item verifies whether the ad repository allows filtering data by
one or more geographic locations where the ads were served. The
assessment should test queries with location filters to confirm that
results match the specified areas.

  - > Yes, through the GUI

  - > Yes, through the API

  - > **No**

**Justification:**

The Pinterest Ads Repository only allows data to be filtered by country.

### ACCURACY

*Accuracy assesses how closely data reflects real-world phenomena,
measuring the correctness of its representation of reality.*

**OC29: Does the platform provide age and gender data on the audiences
of ads?**

This item verifies whether the platform provides data on the age and
gender of audiences reached. The assessment should review the ad records
to confirm that these breakdowns are available and consistently
reported.

  - > Yes, through the GUI

  - > Yes, through the API

  - > **No**

**Justification:**

The Pinterest Ads Repository does not provide any age or gender
information about an ad’s audience.

**OC30: Does the platform provide subnational geographic data on the
audience reached by ads?**

This item verifies whether the platform provides data on the subnational
geographic location of audiences reached. The assessment should review
the ad records to confirm that such location breakdowns are available
and consistently reported.

  - > Yes, through the GUI

  - > Yes, through the API

  - > **No**

**Justification:**

The Pinterest Ads Repository does not provide any subnational location
data about an ad’s audience.

**OC31: Does the platform include data on audience targeting criteria
defined by advertisers?**

This item verifies whether the platform provides data on audience
targeting criteria defined by the advertiser when publishing ads (e.g.,
demographic and geographic segments, as well as interests, attitudes,
behaviors, and keywords). The assessment should review ad records to
confirm that these targeting parameters are available and consistently
reported.

  - > **Yes, through the GUI**

  - > Yes, through the API

  - > No

**Justification:**

The Pinterest Ads Repository provides visibility into the audience
targeting criteria defined by advertisers, such as age, gender,
interests, postal codes, geographic areas, keywords, and other
parameters.

**OC32: Does the platform provide granular volume ranges for ad
impressions?**

This item verifies whether the ad repository provides impression values
for ads, using ranges that closely approximate the actual numbers.
Intervals should be no larger than 10% of the upper bound of the value
range they represent. For example, values up to 1,000 impressions should
be displayed in intervals no larger than 100; between 1,000 and 10,000
in intervals no larger than 1,000; between 10,000 and 100,000 in
intervals no larger than 10,000; between 100,000 and 1 million or above,
in intervals no larger than 100,000. The assessment should measure
whether the reported intervals remain within this threshold across the
different value ranges using the platform’s documentation or available
data interfaces.

  - > Yes, through the GUI

  - > Yes, through the API

  - > **No**

**Justification:**

The Pinterest Ads Repository provides data on ad impressions, but not a
sufficiently granular level.

**OC33: Does the platform provide granular investment ranges for ad
spending?**

This item verifies whether the ad repository provides spending values
for ads, using ranges that closely approximate the actual amounts.
Intervals should be no larger than 10% of the upper bound of the value
range they represent. For example, values up to $100 should be displayed
in intervals no larger than $10; between $100 and $1,000 in intervals no
larger than $100; and between $1,000 and $10,000 in intervals no larger
than $1,000. The assessment should measure whether the reported
intervals remain within this threshold across the different value ranges
using the platform’s documentation or available data interfaces.

  - > Yes, through the GUI

  - > Yes, through the API

  - > **No**

**Justification:**

The Pinterest Ads Repository does not provide data on ad spending in the
European Union.

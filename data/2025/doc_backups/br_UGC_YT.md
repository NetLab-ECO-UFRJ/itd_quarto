**Methodological notes**
========================

SPECIAL CRITERIA
----------------

**SC1: Does the platform offer an API for collecting public
user-generated content data?** - weight 0.30

This item verifies whether the platform provides an API with at least
one endpoint for programmatically extracting public user-generated
content to the users' infrastructure. Public user-generated content is
defined here as any publicly visible publication accessible by any
platform user. The assessment should verify that the endpoint allows
retrieval and storage of this content without requiring privileged or
internal access beyond standard developer registration.

-   **Yes**

-   Yes, but only for approved researchers

-   No

The platform does have an API (YouTube Data v3 API) that allows the
extraction of public UGC.

[[https://developers.google.com/youtube/v3/docs]{.underline}](https://developers.google.com/youtube/v3/docs).

**SC2: Can the full scope of public content data be extracted through
the platform's API?** - weight 0.30

This item verifies whether the platform enables programmatic discovery
and extraction of data from the complete set of public user-generated
content. The assessment should confirm that the API provides access to
all types of public content on the platform, without exclusions or
artificial restrictions that limit data completeness.

-   **Yes**

-   Yes, but only for approved researchers

-   No

YouTube allows searching the entire universe of public videos available
via its API. Therefore, it is possible to use the official API to
structure the programmatic collection of videos and search through any
public channels or videos.

**SC3: Is access to the platform's API free of charge?** - weight 0.30

This item verifies whether API use is free of charge, since even modest
fees can create barriers or force researchers in low-resourced settings
to narrow the scope of their work. The assessment should verify the
platform's documentation and pricing policies to confirm that no fees
are applied for API access.

-   **Yes**

-   Yes, but only for approved researchers

-   No

The use of the YouTube API is limited by daily quotas per project in the
Google Developers Console, but users can obtain credentials for free.

[[https://developers.google.com/youtube/v3/getting-started]{.underline}](https://developers.google.com/youtube/v3/getting-started)

[[https://developers.google.com/youtube/registering\_an\_application]{.underline}](https://developers.google.com/youtube/registering_an_application)

[[https://developers.google.com/youtube/v3/determine\_quota\_cost]{.underline}](https://developers.google.com/youtube/v3/determine_quota_cost)

--

**SC4: Does the platform offer a graphical interface for extracting
data?** - weight 0.10

This item verifies whether the platform offers a graphical interface for
observing and collecting data to the users' infrastructure. The data
should be equivalent to that which is available through the API or the
default user interface. The assessment should confirm the existence of
an official tool, such as a dashboard or export feature, that allows
extracting public content data without programming.

-   Yes

-   Yes, but only for approved researchers

-   **No**

The platform provides no official graphical user interface or tools for
researchers to extract data. All data access is API-based, requiring
technical implementation and programming skills.

OTHER CRITERIA
--------------

### ACCESSIBILITY

*Accessibility measures how easily data can be located, retrieved,
understood and used.*

**OC1: Does the platform offer any type of access to non-public data
(e.g., private groups, not direct messages) to approved researchers?**

This item verifies whether, beyond the retrieval and extraction of
public user-generated content data, the API permits the extraction of
any data from non-public content, such as posts and comments in private
groups or discussion forums, subject to the implementation of adequate
data hashing measures and specific researcher approval. The assessment
should confirm that the API provides such access measures, either
through specific endpoints or other controlled access mechanisms.

-   Yes

-   **No**

YouTube has a research program, but it does not provide access to
non-public data. Regardless of participation in this research program,
access to non-public data through YouTube's API can occur only with the
owner\'s explicit agreement and an authorization token for the request.

[[https://research.youtube/]{.underline}](https://research.youtube/)

[[https://developers.google.com/youtube/v3/docs\#call-the-api]{.underline}](https://developers.google.com/youtube/v3/docs#call-the-api)

--

**OC2: Can the requested data be extracted directly from the platform's
API response?**

This item verifies whether the API returns structured data directly in
its response, rather than only providing a redirect link to the data.
Audiovisual media (e.g., images, videos, and audio) are excluded from
this assessment. The assessment should check sample API responses to
confirm that the requested public data is included in the returned
payload itself.

-   **Yes**

-   No

Responses to requests to the YouTube Data API v3 provide the expected
data in an appropriate format, without requiring redirection. All data
can be directly collected via the API, including title, description, ID,
author, comments, and a link to the audiovisual content.

--

**OC3: Does the platform's API provide a form of authentication that
allows for token renewal without the risk of data loss?**

This item verifies whether the tokens provided for API use can be
renewed without risk of data loss, ensuring continuity and integrity of
data monitoring and extraction. The assessment should check the
platform's documentation or directly observe the authentication and
renewal process to confirm that token updates do not interrupt or
compromise data access.

-   **Yes**

-   No

The collection does not require token renewal, but is limited to the
daily quotas for each project accredited to the user.

\-

**OC4: Does the platform's API offer an endpoint for extracting data
from an individual publication?**

This item verifies whether it is possible to collect data from a
specific public post on the platform using a unique identifier, rather
than relying on search terms or other filters. The assessment should
review the API documentation and test available endpoints to confirm
that an individual publication can be retrieved directly by its unique
identifier.

-   **Yes**

-   No

YouTube Data API v3 can return data from an individual publication as
long as it is publicly available.

---

**OC5: Does the platform's API offer an endpoint for extracting data
from an individual author?**

This item verifies whether it is possible to collect data from public
posts made by a specific author, using their username or unique
identifier. The assessment should review the API documentation and test
relevant endpoints to confirm that data can be retrieved directly for an
individual author.

-   **Yes**

-   No

Every content author has a YouTube channel, and the YouTube Data API v3
provides methods for retrieving data for specific authors. The search
endpoint has a parameter to filter by channel ID. Another way to extract
data from specific users is to get their channel's uploads playlist IDs,
then use those on the "playlist items" endpoint to retrieve metadata for
videos on their respective channels.

[[https://developers.google.com/youtube/v3/docs/search/list]{.underline}](https://developers.google.com/youtube/v3/docs/search/list)

[[https://developers.google.com/youtube/v3/docs/playlistItems]{.underline}](https://developers.google.com/youtube/v3/docs/playlistItems)

**OC6: Does the platform's API provide an endpoint for extracting data
based on search terms?**

This item verifies whether public user-generated content can be
collected via individual or combined search terms, enabling the creation
of datasets of posts mentioning those terms. The assessment should test
search-related endpoints to confirm that queries using keywords return
matching public posts.

-   **Yes**

-   No

The YouTube Data v3 API provides a search option for retrieving video
data that matches specific search terms or expressions.

[[https://developers.google.com/youtube/v3/docs/search]{.underline}](https://developers.google.com/youtube/v3/docs/search)

**---**

**OC7: Does the API use locale-neutral data representations?**

This item verifies whether locale-sensitive data (e.g., timestamps,
currency, numbers) are returned in a locale-neutral format, or whether
relevant locale metadata is included when neutrality is not possible.
The assessment should review the API documentation and inspect sample
responses to confirm the presence of standardized formats or
accompanying metadata.

-   **Yes**

-   No

The API uses internationally standardized, locale-neutral formats for
all temporal and numerical data. All datetime values and video durations
follow the ISO 8601 standard.

[[https://developers.google.com/youtube/v3/docs/videos]{.underline}](https://developers.google.com/youtube/v3/docs/videos)

### ---

### COMPLIANCE

*Compliance refers to how data adheres to standards, conventions and
regulations in a given context. It ensures that data is formatted and
structured in the way it ought to be, according to external or internal
rules.*

**OC8: Does the platform implement a proper deprecation strategy to
avoid breaking client applications while rolling out major changes in
the API?**

This item verifies whether the platform's documentation describes a
deprecation strategy with a grace period before removing features. The
assessment should review changelogs to confirm that deprecated features
are listed with deprecation and removal dates and include migration
instructions. This item applies only to breaking changes that require
client updates, such as endpoint modifications, authentication updates,
or the removal of features.

-   **Yes**

-   No or not applicable

YouTube implements a formal deprecation strategy with defined grace
periods, removal dates, and migration guidance, as well as an RSS feed
enabling update notifications. The official Terms of Service (Section
14.2) state: \"When YouTube intends to make backwards incompatible
changes to YouTube API services, YouTube will announce those changes and
try to continue to maintain the software code for six (6) months from
the date such backwards incompatible changes are announced.\"
Additionally, the revision history page documents all changes with dates
and rationale, clearly identifying deprecation announcements.

[[https://developers.google.com/youtube/terms/api-services-terms-of-service\#youtube-api-services-terms-of-service]{.underline}](https://developers.google.com/youtube/terms/api-services-terms-of-service#youtube-api-services-terms-of-service)

[[https://developers.google.com/youtube/v3/revision\_history]{.underline}](https://developers.google.com/youtube/v3/revision_history)

---\--

**OC9: Is the platform's API documentation published in open access?**

This item verifies whether the platform makes its API documentation
openly available on the internet, without requiring registration or
login. The assessment should check whether full documentation can be
accessed freely online without requiring account creation or
authentication.

-   **Yes**

-   No

The YouTube Data API v3 documentation can be accessed without
authentication.
[[https://developers.google.com/youtube/v3/docs/]{.underline}](https://developers.google.com/youtube/v3/docs/)

--

**OC10: Is the platform's API documentation clearly written and
exemplified?**

This item verifies whether the documentation for the platform's API is
clear, complete, and provides practical implementation examples. The
assessment should review the documentation to confirm the presence of
detailed explanations, structured references, and sample code or queries
that illustrate correct usage.

-   **Yes**

-   No

The YouTube API documentation provides clear examples of its use,
including the different types of objects returned and the expected
responses.

**---\
**

**OC11: Does the platform's API documentation include or link to the API
terms of use?**

This item verifies whether the documentation clearly states or links to
the terms of use governing the API and its legal aspects. The assessment
should review the documentation to confirm the presence of explicit
legal terms that define permitted use and restrictions.

-   **Yes**

-   No

The YouTube API documentation details its terms of use, including those
specific to regions of the world. The document is linked at the bottom
of the API documentation.

[[https://developers.google.com/youtube/v3/docs]{.underline}](https://developers.google.com/youtube/v3/docs)

[[https://developers.google.com/youtube/terms]{.underline}](https://developers.google.com/youtube/terms)

---

**OC12: Does the platform's API documentation detail the response format
of each endpoint?**

This item verifies whether the API documentation specifies the response
format for each endpoint, including examples and potential error codes.
The assessment should review the documentation to confirm that, in all
or most cases, response structures are explicitly described and
illustrated with sample outputs.

-   **Yes**

-   No

Each method in the YouTube Data API v3 includes an example of its
response format.

[[https://developers.google.com/youtube/v3/docs/videos\#resource-representation]{.underline}](https://developers.google.com/youtube/v3/docs/videos#resource-representation)

[[https://developers.google.com/youtube/v3/docs/videos/list\#response]{.underline}](https://developers.google.com/youtube/v3/docs/videos/list#response)

---

**OC13: Does the platform provide its API documentation in the official
languages of the assessed region?**

This item verifies whether the platform provides its API documentation
in the official languages of the assessed region. The assessment should
review the documentation to confirm that complete and up-to-date
versions are available in those languages.

-   **Yes**

-   No

Several possible translations of the documentation are available,
including Portuguese. The language can be chosen in the upper-right
corner of the page.

[[https://developers.google.com/youtube/v3/docs/videos?hl=pt-br]{.underline}](https://developers.google.com/youtube/v3/docs/videos?hl=pt-br)

---

**OC14: Does the platform's API documentation detail the quota or rate
limits applicable to each available endpoint?**

This item verifies whether the documentation specifies the limits for
each endpoint. Rate limits define the maximum number of requests allowed
within a given period (e.g., 1,000 requests per hour), while quotas set
overall usage limits (e.g., total API calls per month). The assessment
should review the documentation to confirm that usage limits are clearly
stated, including variations by authentication level or endpoint type.

-   **Yes**

-   No

The YouTube Data API v3 has a default quota of 10,000 points per day,
with each request consuming a portion of this quota. Different methods
may have different costs, which are detailed on their respective
documentation pages. It is also possible to increase a project\'s daily
quota by completing an audit form or participating in YouTube's
researcher program.

[[https://developers.google.com/youtube/v3/getting-started\#quota]{.underline}](https://developers.google.com/youtube/v3/getting-started#quota)

[[https://support.google.com/youtube/contact/yt\_api\_form]{.underline}](https://support.google.com/youtube/contact/yt_api_form)

[[https://research.youtube/]{.underline}](https://research.youtube/)

[[https://developers.google.com/youtube/v3/docs/comments/list]{.underline}](https://developers.google.com/youtube/v3/docs/comments/list)

---

**OC15: Does the platform provide a way to label content that has been
generated with artificial intelligence?**

This item verifies whether the platform automatically flags, or allows
users to flag, AI-generated content, and whether this information is
given in the API response. The assessment should review the
documentation and test API outputs to confirm that these flags are
included in the extracted data.

-   Yes

-   **No**

YouTube lacks API-level methods for detecting or labeling AI-generated
content despite the existence of platform-level features. We found no
official policy or technical specification for AI-generated content in
the YouTube Data API v3 documentation and terms of service.

[[https://support.google.com/youtube/answer/14328491]{.underline}](https://support.google.com/youtube/answer/14328491)

---

### COMPLETENESS

*Completeness refers to how closely the data reflects the dimensions of
what it represents (in breadth, depth and scope).*

**OC16: Can data from a publication's comments be extracted using the
platform's API?**

This item verifies whether comment data, including their content, can be
extracted when available on the platform, either together with
publication data or with a dedicated endpoint. The assessment should
test relevant endpoints to confirm that comments are retrievable as
structured data. This item does not apply to platforms that do not have
commenting features.

-   **Yes**

-   No

-   Not applicable

YouTube Data API v3 provides an endpoint to extract comment threads from
videos, each containing the top-level comment and up to 5 replies. If
the top-level comment has more than 5 replies, they can be extracted
using the API\'s comments endpoint, filtering by the top-level comment
ID (parent comment ID).

[[https://developers.google.com/youtube/v3/guides/implementation/comments]{.underline}](https://developers.google.com/youtube/v3/guides/implementation/comments)

[[https://developers.google.com/youtube/v3/docs/commentThreads/list]{.underline}](https://developers.google.com/youtube/v3/docs/commentThreads/list)

[[https://developers.google.com/youtube/v3/docs/comments]{.underline}](https://developers.google.com/youtube/v3/docs/comments)

---

**OC17: Can data from temporary content be extracted through the
platform's API?**

This item verifies whether the platform's API provides at least one
endpoint for collecting data from temporary publications (e.g., stories,
ephemeral messages). The assessment should test endpoints to confirm
whether this type of short-lived content can be retrieved as structured
data before it expires. This item does not apply to platforms that do
not have temporary content features.

-   Yes

-   No

-   **Not applicable**

Currently, YouTube does not have built-in support for ephemeral content.
The platform deprecated its Stories feature in June 2023.

[[https://support.google.com/youtube/thread/217640760/youtube-stories-are-going-away-on-6-26-2023]{.underline}](https://support.google.com/youtube/thread/217640760/youtube-stories-are-going-away-on-6-26-2023)

----

**OC18: Can historical data be extracted through the platform's API?**

This item verifies whether the API provides endpoints that allow for a
specified time range, going back more than one year from the time the
request is made, to collect public user-generated content data. The
assessment should review test endpoints to confirm that historical data
more than 12 months prior to the analysis can be retrieved.

-   **Yes**

-   No

The search endpoint includes parameters for selecting a time range for
videos, channels, and playlists. Therefore, the API allows collecting
data from any videos available on the platform, regardless of their
publication date. However, Developer Policies (Section III.E.4) demands
API clients to "either delete or refresh stored resource metadata from
that API after 30 days,\" preventing long-term historical analysis
without continuous re-fetching. Also, from our experience, paginating a
channel's videos from their uploads playlist (a possible endpoint for
accessing a channel's historic data) can return no more than 20,000
videos, so while this is a reasonably high count of videos, if a larger
channel's complete video history is needed, this playlist endpoint might
be insufficient.

[[https://developers.google.com/youtube/terms/developer-policies\#e.-handling-youtube-data-and-content]{.underline}](https://developers.google.com/youtube/terms/developer-policies#e.-handling-youtube-data-and-content)

---\-\-\-\-\-\-\-\--

**OC19: Is the number of requests allowed by the API sufficient for
monitoring more than 10,000 publications in 24 hours?**

This item verifies whether data can be extracted without interruption
and losses through the platform's API for requests that accumulate more
than 10,000 publications in 24 hours. The assessment should test the API
to confirm that this volume of data can be collected continuously.

-   Yes

-   **No**

The search list endpoint (for searching videos by query or channel ID)
consumes 100 of the 10,000 daily points per request. Since each request
can only return up to 50 videos, the maximum number of videos one can
get by this method, per day, is 5,000. Therefore, if a monitoring task
depends on search queries, this approach is insufficient to gather more
than 5,000 publications per day. Also, there is a cap for the number of
result pages retrieved for a set of parameters when using the search
list endpoint. Our tests had to change parameters to get more data pages
and hit the daily quota limit; otherwise, the collected video limit
would be even lower if we were only allowed to use fixed parameters on
this endpoint. However, the API\'s daily quota is sufficient to monitor
more than 10,000 publications in 24 hours for other endpoints that do
not depend on search (e.g., *videos.list* or *playlistItems.list*).

---

### CONSISTENCY

*This dimension tracks whether the data always presents the same values,
the same format in every occurrence and if it is compatible with the
previous data.*

**OC20: Are the results returned by the API consistently reproducible?**

This item verifies whether data extracted via the platform's API at any
given time is consistent with other collections performed similarly,
including content that has been deleted between collections. The
assessment should conduct repeated test queries to confirm the
reproducibility of results or ground the response based on recent (less
than 2 years) experiments published in peer-reviewed journals.

-   Yes

-   **No**

The documentation does not guarantee that API results are consistently
reproducible and explicitly acknowledges approximations in key metrics.
We made the same request to the search list endpoint multiple times,
using "relevance" for the order parameter. The results differed in the
order of the returned items. Additionally, after deletion, YouTube
videos and comments cannot be queried.

**---**

**OC21: Is the data returned by the platform's API consistent with the
parameters and filters used in the request?**

This item verifies whether the data extracted through the API accurately
reflects the parameters and filters specified in the request. The
assessment should conduct repeated test queries to confirm the
consistency of results or ground the response based on recent (less than
2 years) experiments published in peer-reviewed journals.

-   Yes

-   **No**

There are frequent inconsistencies, even in collections using fixed
parameters. In our tests, we found that the YouTube API does not
necessarily honor user-defined filters. For instance, the documentation
about the "relevanceLanguage" filter states that "results in other
languages will still be returned if they are highly relevant to the
search query term", meaning the language filter operates as a soft
preference rather than a strict constraint, allowing inconsistent
results. In our tests, we confirmed that when requesting videos in
Portuguese, one of the resulting items used English for its description
and title. Also, comments were written in English. Although the video
had no spoken dialogue ---only images and English text ---the previous
statements already indicate that the video is targeted for
English-speaking audiences. Recent academic studies have also addressed
these consistency issues.

[[https://developers.google.com/youtube/v3/docs/search/list]{.underline}](https://developers.google.com/youtube/v3/docs/search/list)

[[https://arxiv.org/abs/2506.04422]{.underline}](https://arxiv.org/abs/2506.04422)

[[https://arxiv.org/pdf/2506.11727]{.underline}](https://arxiv.org/pdf/2506.11727)

---

### RELEVANCE

*Relevance evaluates how helpful the data is and how applicable for use
it is, also considering future applications. This dimension also
evaluates the extent to which the content and coverage of data meet the
user's needs.*

**OC22: Does the data extracted by the platform's API reflect what is
displayed on its user interface?**

This item verifies whether the data returned by the API corresponds to
the information displayed on the platform's user interface at all levels
of detail. The assessment should compare API responses with the user
interface to confirm that key elements, such as authorship, complete
content, interaction counts (e.g., comments, shares, replies), and
referenced content (e.g., shares, mentions), are fully represented.

-   **Yes**

-   No

We ran tests comparing metrics from video and live streamings and
confirmed that the numbers returned by the API are consistent with those
on the user interface, although they are rounded and might not reflect
the actual content available (e.g., total comment replies on the user
interface can differ from the actual retrievable replies available via
API).

--

**OC23: Does the platform's API allow for filtering data based on
publisher location?**

This item verifies whether the API supports applying location-based
filters to data extraction. The assessment should test the endpoint for
the main content type to confirm that data on public posts can be
filtered by publisher location.

-   Yes

-   **No**

The API does not support filtering by channel/publisher location. This
feature was deprecated from API v2. Currently, the "search.list"
endpoint includes a location parameter, but this applies to video
geographic metadata (where content was filmed), not channel/publisher
location. The "regionCode" parameter \"instructs the API to return
search results for videos that can be viewed in the specified country\",
filtering by content availability region, not by publishers' location.

[https://developers.google.com/youtube/v3/revision\_history\#march-11,-2015]{.underline}

[[https://developers.google.com/youtube/v3/docs/search/list]{.underline}](https://developers.google.com/youtube/v3/docs/search/list)

**OC24: Does the platform's API allow for filtering data based on
content language?**

This item verifies whether the API allows for applying language-based
filters to data extraction. The assessment should test the endpoint for
the main content type to confirm that public post data can be filtered
by content language.

-   **Yes**

-   No

The API provides language-related filter parameters, but these influence
relevance sorting rather than implementing strict filters. In our tests,
when requesting videos in Portuguese, some videos were in English, and
while some had their pages automatically translated to Portuguese
(including the audio tracks), others did not.

[[https://developers.google.com/youtube/v3/docs/search/list\#parameters]{.underline}](https://developers.google.com/youtube/v3/docs/search/list#parameters)

**---**

**OC25: Does the platform's API allow for filtering data by specific
time periods?**

This item verifies whether the API allows applying temporal filters to
data extraction. The assessment should test the endpoint for the main
content type to confirm that public post data can be filtered by custom
time ranges.

-   **Yes**

-   No

The API provides comprehensive temporal filtering through dedicated
date-time parameters.

[[https://developers.google.com/youtube/v3/docs/search/list]{.underline}](https://developers.google.com/youtube/v3/docs/search/list)

---

### TIMELINESS

*Timeliness refers to how current and available the data is when it is
requested. Delays in recall render current data useless, as the data is
no longer required.*

**OC26: Can data from newly published content be extracted from the
platform's API in near real time?**

This item verifies whether the API allows the collection of data from
specific content within one hour of its publication. The assessment
should test the endpoint for the main content type to confirm that it
allows the ready extraction of recent public posts data.

-   **Yes**

-   No

It is possible to extract data from the platform as soon as the content
is published.

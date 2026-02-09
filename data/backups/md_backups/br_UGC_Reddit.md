# **Formula/weighting method**

## SPECIAL CRITERIA

**SC1: Does the platform offer an API for collecting public
user-generated content data?** - weight 0.30

This item verifies whether the platform provides an API with at least
one endpoint for programmatically extracting public user-generated
content to the users’ infrastructure. Public user-generated content is
defined here as any publicly visible publication accessible by any
platform user. The assessment should verify that the endpoint allows
retrieval and storage of this content without requiring privileged or
internal access beyond standard developer registration.

  - > **Yes**

  - > Yes, but only for approved researchers

  - > No

Reddit provides a Data API that enables programmatic extraction of
public user-generated content, including posts, comments, and subreddit
information.

[<span class="underline">https://www.reddit.com/dev/api/</span>](https://www.reddit.com/dev/api/)

[<span class="underline">https://support.reddithelp.com/hc/en-us/articles/16160319875092-Reddit-Data-API-Wiki</span>](https://support.reddithelp.com/hc/en-us/articles/16160319875092-Reddit-Data-API-Wiki)

[<span class="underline">https://www.reddit.com/r/reddit.com/wiki/api/\#wiki\_read\_the\_full\_api\_terms\_and\_sign\_up\_for\_usage</span>](https://www.reddit.com/r/reddit.com/wiki/api/#wiki_read_the_full_api_terms_and_sign_up_for_usage)

**SC2: Can the full scope of public content data be extracted through
the platform’s API?** - weight 0.30

This item verifies whether the platform enables programmatic discovery
and extraction of data from the complete set of public user-generated
content. The assessment should confirm that the API provides access to
all types of public content on the platform, without exclusions or
artificial restrictions that limit data completeness.

  - > Yes

  - > Yes, but only for approved researchers

  - > **No**

It’s not possible to retrieve the full scope of public data through the
platform’s API. When trying to collect historical data, only a subset
was returned by the search endpoint. Our test requested all posts using
“brexit” as a search term, without specifying a time period to
restrict results, the only parameter that was set besides the query was
sorting, because this is a required parameter. In the first request
attempt, we used the wrapper’s default (relevance), and in the second
attempt, we used the “new” sorting option.

The total posts retrieved by the requests was different in quantity, as
well as the posts, and only a few posts were retrieved by both requests.
Changing the sorting parameter shouldn’t affect the quantity of data
retrieved.

**SC3: Is access to the platform’s API free of charge?** - weight 0.30

This item verifies whether API use is free of charge, since even modest
fees can create barriers or force researchers in low-resourced settings
to narrow the scope of their work. The assessment should verify the
platform’s documentation and pricing policies to confirm that no fees
are applied for API access.

  - **Yes**

  - Yes, but only for approved researchers

  - No

Reddit offers free APIs for non-commercial and research uses under
specific conditions, quota limits, and constraints.

**SC4: Does the platform offer a graphical interface for extracting
data?** - weight 0.10

This item verifies whether the platform offers a graphical interface for
observing and collecting data to the users’ infrastructure. The data
should be equivalent to that which is available through the API or the
default user interface. The assessment should confirm the existence of
an official tool, such as a dashboard or export feature, that allows
extracting public content data without programming.

  - > Yes

  - > Yes, but only for approved researchers

  - > **No**

The platform provides no official graphical user interface or tools for
researchers to extract data. All data access is API-based, requiring
technical implementation and programming skills.

## OTHER CRITERIA

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

  - > Yes

  - > **No**

Reddit launched a Researchers Beta Program in 2024, but the initiative
has been inactive for months, and we could not find evidence that it
provided access to non-public data.

[<span class="underline">https://www.reddit.com/r/reddit4researchers/comments/1co0mqa/our\_plans\_for\_researchers\_on\_reddit/</span>](https://www.reddit.com/r/reddit4researchers/comments/1co0mqa/our_plans_for_researchers_on_reddit/)

[<span class="underline">https://www.reddit.com/r/reddit4researchers/comments/1ffd56x/reddit\_for\_researchers\_beta\_program\_were\_live/</span>](https://www.reddit.com/r/reddit4researchers/comments/1ffd56x/reddit_for_researchers_beta_program_were_live/)

[<span class="underline">https://www.reddit.com/r/reddit4researchers/comments/1g5znj3/the\_reddit\_for\_researchers\_beta\_program\_is\_growing/</span>](https://www.reddit.com/r/reddit4researchers/comments/1g5znj3/the_reddit_for_researchers_beta_program_is_growing/)

**OC2: Can the requested data be extracted directly from the platform’s
API response?**

This item verifies whether the API returns structured data directly in
its response, rather than only providing a redirect link to the data.
Audiovisual media (e.g., images, videos, and audio) are excluded from
this assessment. The assessment should check sample API responses to
confirm that the requested public data is included in the returned
payload itself.

  - > **Yes**

  - > No

The API returns data directly in JSON format within the API response
payload for all endpoints tested.

[<span class="underline">https://www.reddit.com/dev/api/</span>](https://www.reddit.com/dev/api/)

**OC3: Does the platform’s API provide a form of authentication that
allows for token renewal without the risk of data loss?**

This item verifies whether the tokens provided for API use can be
renewed without risk of data loss, ensuring continuity and integrity of
data monitoring and extraction. The assessment should check the
platform’s documentation or directly observe the authentication and
renewal process to confirm that token updates do not interrupt or
compromise data access.

  - > **Yes**

  - > No

To access the API, it is necessary to create a developer or research
account, and once approved, the API can be used by informing the client
ID, secret, and user agent. No token renewal is needed for data access.

**OC4: Does the platform’s API offer an endpoint for extracting data
from an individual publication?**

This item verifies whether it is possible to collect data from a
specific public post on the platform using a unique identifier, rather
than relying on search terms or other filters. The assessment should
review the API documentation and test available endpoints to confirm
that an individual publication can be retrieved directly by its unique
identifier.

  - > **Yes**

  - > No

The platform provides endpoints for retrieving individual posts using
unique identifiers or through the post url/permalink.

[<span class="underline">https://www.reddit.com/dev/api/\#GET\_comments\_{article</span>](https://www.reddit.com/dev/api/#GET_comments_%7Barticle)}

**OC5: Does the platform’s API offer an endpoint for extracting data
from an individual author?**

This item verifies whether it is possible to collect data from public
posts made by a specific author, using their username or unique
identifier. The assessment should review the API documentation and test
relevant endpoints to confirm that data can be retrieved directly for an
individual author.

  - > **Yes**

  - > No

The API provides endpoints for retrieving posts by specific authors.
Posts and comments can be filtered by author username, allowing the
collection of all public content from a specific user.

[<span class="underline">https://www.reddit.com/dev/api/\#GET\_user\_{username}\_submitted</span>](https://www.reddit.com/dev/api/#GET_user_%7Busername%7D_submitted)

**OC6: Does the platform’s API provide an endpoint for extracting data
based on search terms?**

This item verifies whether public user-generated content can be
collected via individual or combined search terms, enabling the creation
of datasets of posts mentioning those terms. The assessment should test
search-related endpoints to confirm that queries using keywords return
matching public posts.

  - > **Yes**

  - > No

The API includes search functionality through a dedicated endpoint.

[<span class="underline">https://www.reddit.com/dev/api/\#GET\_search</span>](https://www.reddit.com/dev/api/#GET_search)

**OC7: Does the API use locale-neutral data representations?**

This item verifies whether locale-sensitive data (e.g., timestamps,
currency, numbers) are returned in a locale-neutral format, or whether
relevant locale metadata is included when neutrality is not possible.
The assessment should review the API documentation and inspect sample
responses to confirm the presence of standardized formats or
accompanying metadata.

  - > **Yes**

  - > No

The API uses Unix epoch timestamps (UTC-based integers) for all temporal
data.

[<span class="underline">https://praw.readthedocs.io/en/stable/search.html?q=%22Unix+Time%22\&check\_keywords=yes\&area=default\#</span>](https://praw.readthedocs.io/en/stable/search.html?q=%22Unix+Time%22&check_keywords=yes&area=default#)

### COMPLIANCE

*Compliance refers to how data adheres to standards, conventions and
regulations in a given context. It ensures that data is formatted and
structured in the way it ought to be, according to external or internal
rules.*

**OC8: Does the platform implement a proper deprecation strategy to
avoid breaking client applications while rolling out major changes in
the API?**

This item verifies whether the platform’s documentation describes a
deprecation strategy with a grace period before removing features. The
assessment should review changelogs to confirm that deprecated features
are listed with deprecation and removal dates and include migration
instructions. This item applies only to breaking changes that require
client updates, such as endpoint modifications, authentication updates,
or the removal of features.

  - > Yes

  - > **No or not applicable**

Reddit’s documentation states that “changes to the API can happen
without warning if necessary”.

[<span class="underline">https://github.com/reddit-archive/reddit/wiki/API</span>](https://github.com/reddit-archive/reddit/wiki/API)

**OC9: Is the platform’s API documentation published in open access?**

This item verifies whether the platform makes its API documentation
openly available on the internet, without requiring registration or
login. The assessment should check whether full documentation can be
accessed freely online without requiring account creation or
authentication.

  - > **Yes**

  - > No

The API documentation is publicly accessible without requiring
registration or login.

[<span class="underline">https://www.reddit.com/dev/api/</span>](https://www.reddit.com/dev/api/)

[<span class="underline">https://support.reddithelp.com/hc/en-us/articles/16160319875092-Reddit-Data-API-Wiki</span>](https://support.reddithelp.com/hc/en-us/articles/16160319875092-Reddit-Data-API-Wiki)

[<span class="underline">https://github.com/reddit-archive/reddit/wiki/API</span>](https://github.com/reddit-archive/reddit/wiki/API)

**OC10: Is the platform’s API documentation clearly written and
exemplified?**

This item verifies whether the documentation for the platform’s API is
clear, complete, and provides practical implementation examples. The
assessment should review the documentation to confirm the presence of
detailed explanations, structured references, and sample code or queries
that illustrate correct usage.

  - > Yes

  - > **No**

The documentation is automatically-generated, hard to navigate, and
lacks comprehensive examples and a clear structure. Reddit does not
provide an OpenAPI specification, further limiting documentation
clarity.

[<span class="underline">https://www.reddit.com/dev/api/</span>](https://www.reddit.com/dev/api/)

**OC11: Does the platform’s API documentation include or link to the API
terms of use?**

This item verifies whether the documentation clearly states or links to
the terms of use governing the API and its legal aspects. The assessment
should review the documentation to confirm the presence of explicit
legal terms that define permitted use and restrictions.

  - > **Yes**

  - > No

The wiki with human-generated documentation clearly links to the
platform’s terms of service at the top of the page.

[<span class="underline">https://support.reddithelp.com/hc/en-us/articles/16160319875092-Reddit-Data-API-Wiki</span>](https://support.reddithelp.com/hc/en-us/articles/16160319875092-Reddit-Data-API-Wiki)

**OC12: Does the platform’s API documentation detail the response format
of each endpoint?**

This item verifies whether the API documentation specifies the response
format for each endpoint, including examples and potential error codes.
The assessment should review the documentation to confirm that, in all
or most cases, response structures are explicitly described and
illustrated with sample outputs.

  - > Yes

  - > **No**

While the documentation lists available endpoints, it does not
consistently provide detailed specifications for response formats or
comprehensive examples.

[<span class="underline">https://www.reddit.com/dev/api/</span>](https://www.reddit.com/dev/api/)

**OC13: Does the platform provide its API documentation in the official
languages of the assessed region?**

This item verifies whether the platform provides its API documentation
in the official languages of the assessed region. The assessment should
review the documentation to confirm that complete and up-to-date
versions are available in those languages.

  - > Yes

  - > **No**

The API documentation is available only in English.

[<span class="underline">https://www.reddit.com/dev/api/</span>](https://www.reddit.com/dev/api/)

**OC14: Does the platform’s API documentation detail the quota or rate
limits applicable to each available endpoint?**

This item verifies whether the documentation specifies the limits for
each endpoint. Rate limits define the maximum number of requests allowed
within a given period (e.g., 1,000 requests per hour), while quotas set
overall usage limits (e.g., total API calls per month). The assessment
should review the documentation to confirm that usage limits are clearly
stated, including variations by authentication level or endpoint type.

  - > **Yes**

  - > No

The documentation clearly specifies rate limits.

[<span class="underline">https://support.reddithelp.com/hc/en-us/articles/16160319875092-Reddit-Data-API-Wiki</span>](https://support.reddithelp.com/hc/en-us/articles/16160319875092-Reddit-Data-API-Wiki)

**OC15: Does the platform provide a way to label content that has been
generated with artificial intelligence?**

This item verifies whether the platform automatically flags, or allows
users to flag, AI-generated content, and whether this information is
given in the API response. The assessment should review the
documentation and test API outputs to confirm that these flags are
included in the extracted data.

  - > Yes

  - > **No**

Reddit's official API documentation contains no mention of AI-generated
content flags or labels in API responses. While Reddit partnered with
researchers to develop “models for detecting and managing AI-generated
content”, this feature is not documented as available in the API, and no
fields for AI-content identification appear in the documented response
formats.

[<span class="underline">https://www.reddit.com/dev/api</span>](https://www.reddit.com/dev/api)

[<span class="underline">https://support.reddithelp.com/hc/en-us/articles/16160319875092-Reddit-Data-API-Wiki</span>](https://support.reddithelp.com/hc/en-us/articles/16160319875092-Reddit-Data-API-Wiki)

[<span class="underline">https://www.reddit.com/r/reddit4researchers/comments/1g5znj3/the\_reddit\_for\_researchers\_beta\_program\_is\_growing/</span>](https://www.reddit.com/r/reddit4researchers/comments/1g5znj3/the_reddit_for_researchers_beta_program_is_growing/)

### COMPLETENESS

*Completeness refers to how closely the data reflects the dimensions of
what it represents (in breadth, depth and scope).*

**OC16: Can data from a publication’s comments be extracted using the
platform’s API?**

This item verifies whether comment data, including their content, can be
extracted when available on the platform, either together with
publication data or with a dedicated endpoint. The assessment should
test relevant endpoints to confirm that comments are retrievable as
structured data. This item does not apply to platforms that do not have
commenting features.

  - > **Yes**

  - > No

  - > Not applicable

The platform provides comprehensive access to comment data. Comments can
be retrieved via endpoints that return both the post and its comment
tree, as well as dedicated search endpoints for comments.

[<span class="underline">https://www.reddit.com/dev/api/\#GET\_comments\_{article</span>](https://www.reddit.com/dev/api/#GET_comments_%7Barticle)}

[<span class="underline">https://www.reddit.com/dev/api/\#GET\_user\_{username}\_comments</span>](https://www.reddit.com/dev/api/#GET_user_%7Busername%7D_comments)

**OC17: Can data from temporary content be extracted through the
platform’s API?**

This item verifies whether the platform’s API provides at least one
endpoint for collecting data from temporary publications (e.g., stories,
ephemeral messages). The assessment should test endpoints to confirm
whether this type of short-lived content can be retrieved as structured
data before it expires. This item does not apply to platforms that do
not have temporary content features.

  - > Yes

  - > No

  - > **Not applicable**

Reddit does not have temporary or ephemeral content.

**OC18: Can historical data be extracted through the platform’s API?**

This item verifies whether the API provides endpoints that allow for a
specified time range, going back more than one year from the time the
request is made, to collect public user-generated content data. The
assessment should review test endpoints to confirm that historical data
more than 12 months prior to the analysis can be retrieved.

  - > **Yes**

  - > No

It is possible to extract historical data, though there is a limit of
1000 items returned across all listing endpoints.

It is possible to extract historical data, though it doesn’t seem to
retrieve the full scope of historical data, only a subset that is
influenced by the sort parameter, as explained in SC02.

[<span class="underline">https://www.reddit.com/dev/api/\#GET\_search</span>](https://www.reddit.com/dev/api/#GET_search)

**OC19: Is the number of requests allowed by the API sufficient for
monitoring more than 10,000 publications in 24 hours?**

This item verifies whether data can be extracted without interruption
and losses through the platform’s API for requests that accumulate more
than 10,000 publications in 24 hours. The assessment should test the API
to confirm that this volume of data can be collected continuously.

  - > **Yes**

  - > No

Reddit’s Data API free tier currently limits 100 queries per minute
(QPM) per OAuth client ID. This translates to 144,000 requests per
24-hour period.

We conducted a two-hour test requesting data through the subreddit
stream endpoint and it was enough to collect more than 10.000
publications, although no data older than the job start time was
retrieved.

[<span class="underline">https://support.reddithelp.com/hc/en-us/articles/16160319875092-Reddit-Data-API-Wiki</span>](https://support.reddithelp.com/hc/en-us/articles/16160319875092-Reddit-Data-API-Wiki)

### CONSISTENCY

*This dimension tracks whether the data always presents the same values,
the same format in every occurrence and if it is compatible with the
previous data.*

**OC20: Are the results returned by the API consistently reproducible?**

This item verifies whether data extracted via the platform’s API at any
given time is consistent with other collections performed similarly,
including content that has been deleted between collections. The
assessment should conduct repeated test queries to confirm the
reproducibility of results or ground the response based on recent (less
than 2 years) experiments published in peer-reviewed journals.

  - > **Yes**

  - > No

We ran a test that made 5 requests to the search endpoint, using the
same parameters and search term, with 1 minute between each request. All
responses returned the same data.

**OC21: Is the data returned by the platform’s API consistent with the
parameters and filters used in the request?**

This item verifies whether the data extracted through the API accurately
reflects the parameters and filters specified in the request. The
assessment should conduct repeated test queries to confirm the
consistency of results or ground the response based on recent (less than
2 years) experiments published in peer-reviewed journals.

  - > **Yes**

  - > No

Although there are only a few parameters available to filter data, we
tested two (a time filter to collect data from the day before and
sorting by newest data), and both responses were consistent with the
request parameters.

### RELEVANCE

*Relevance evaluates how helpful the data is and how applicable for use
it is, also considering future applications. This dimension also
evaluates the extent to which the content and coverage of data meet the
user’s needs.*

**OC22: Does the data extracted by the platform’s API reflect what is
displayed on its user interface?**

This item verifies whether the data returned by the API corresponds to
the information displayed on the platform’s user interface at all levels
of detail. The assessment should compare API responses with the user
interface to confirm that key elements, such as authorship, complete
content, interaction counts (e.g., comments, shares, replies), and
referenced content (e.g., shares, mentions), are fully represented.

  - > **Yes**

  - > No

All key elements that are shown in the user interface are present in the
API response.

**OC23: Does the platform’s API allow for filtering data based on
publisher location?**

This item verifies whether the API supports applying location-based
filters to data extraction. The assessment should test the endpoint for
the main content type to confirm that data on public posts can be
filtered by publisher location.

  - > Yes

  - > **No**

The platform does not provide any location-based filtering parameters
for posts or comments.

[<span class="underline">https://www.reddit.com/dev/api/</span>](https://www.reddit.com/dev/api/)

**OC24: Does the platform’s API allow for filtering data based on
content language?**

This item verifies whether the API allows for applying language-based
filters to data extraction. The assessment should test the endpoint for
the main content type to confirm that public post data can be filtered
by content language.

  - > Yes

  - > **No**

The platform does not provide any language-based filtering parameters
for posts or comments.

**OC25: Does the platform’s API allow for filtering data by specific
time periods?**

This item verifies whether the API allows applying temporal filters to
data extraction. The assessment should test the endpoint for the main
content type to confirm that public post data can be filtered by custom
time ranges.

  - > Yes

  - > **No**

While Reddit's API supports time-based filtering, it only accepts
predefined periods (hour, day, week, month, year, all) and does not
support custom date ranges with specific start and end dates.

### TIMELINESS

*Timeliness refers to how current and available the data is when it is
requested. Delays in recall render current data useless, as the data is
no longer required.*

**OC26: Can data from newly published content be extracted from the
platform’s API in near real time?**

This item verifies whether the API allows the collection of data from
specific content within one hour of its publication. The assessment
should test the endpoint for the main content type to confirm that it
allows the ready extraction of recent public posts data.

  - > **Yes**

  - > No

The platform provides near real-time access to newly published content.
The /new endpoint provides access to posts sorted chronologically by
creation time, and the API reflects new posts almost immediately after
publication.

[<span class="underline">https://www.reddit.com/dev/api/\#GET\_new</span>](https://www.reddit.com/dev/api/#GET_new)

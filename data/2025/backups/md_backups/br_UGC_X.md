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

This criterion requires code development [[Rafael Tadeu Cardoso dos
Santos]{.underline}](mailto:rafael.cardoso@netlab.eco.ufrj.br)

**Justification:**

X/Twitter provides a longstanding API ([[X,
n.d.-l]{.underline}](https://developer.x.com/en/docs/x-api)) that has
been extensively documented and widely used for academic research (see
[[Dongo et al.,
2020]{.underline}](https://doi.org/10.1145/3428757.3429104)). It remains
accessible to anyone with a registered developer account, although, as
will be discussed further, such access is now mostly paid ([[Mimizuka et
al., 2025]{.underline}](https://arxiv.org/abs/2505.09877)).

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

**Justification:**

Historically, X/Twitter has ensured that any public conversation
published on the platform generates publicly available data that can be
accessed and explored by developers through its API ([[Johnson,
2018]{.underline}](https://blog.x.com/developer/en_us/topics/tools/2018/twitter-developer-platform-and-user-privacy)).

**SC3: Is access to the platform's API free of charge?** - weight 0.30

This item verifies whether API use is free of charge, since even modest
fees can create barriers or force researchers in low-resourced settings
to narrow the scope of their work. The assessment should verify the
platform's documentation and pricing policies to confirm that no fees
are applied for API access.

-   Yes

-   Yes, but only for approved researchers

-   **No**

**Justification:**

In February 2023, X/Twitter announced that it would begin charging for
the use of its API ([[Nóbrega,
2023]{.underline}](https://desinformante.com.br/twitter-api/)), which
had previously been mostly free of charge ([[Mimizuka et al.,
2025]{.underline}](https://arxiv.org/abs/2505.09877)). Currently, access
to the API is divided into four levels: (i) Free, which allows retrieval
of data from up to 100 posts per month; (ii) Basic, which, at a cost of
USD 200 per month, allows retrieval of up to 15,000 posts; (iii) Pro,
which, at a cost of USD 5,000 per month, allows retrieval of up to
1,000,000 posts; and (iv) Enterprise, for which pricing and usage limits
are negotiated directly with the platform ([[X,
n.d.-a]{.underline}](https://docs.x.com/x-api/getting-started/about-x-api)).
As the free plan offers extremely limited capabilities and is presented
by the platform itself as a testing tier ([[X,
n.d.-l]{.underline}](https://developer.x.com/en/docs/x-api)), we do not
consider it sufficient to characterize access to the platform's API as
free of charge.

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

**Justification:**

X/Twitter does not provide a graphical interface for accessing or
extracting public user-generated content data.

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

**Justification:**

X/Twitter does not provide any form of access to or extraction of
non-public user-generated content data in Brazil ([[X,
n.d.-m]{.underline}](https://docs.x.com/x-api/fundamentals/data-dictionary)).

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

This criterion requires code development [[Rafael Tadeu Cardoso dos
Santos]{.underline}](mailto:rafael.cardoso@netlab.eco.ufrj.br)

**Justification:**

To use the Twitter/X API, many endpoints allow you to specify which
additional fields you want to retrieve by using the *tweet.fields*
parameter. This parameter accepts a comma-separated list of field names
representing the specific tweet attributes you are interested in (e.g.,
created\_at, author\_id, public\_metrics). When you include this
parameter in your request, the API response should return the tweets
with the requested fields included. However, not all fields will appear
in the response, as some may not be relevant to the data returned by the
endpoint.

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

**Justification:**

If we consider only the limits of each tier, then tokens can be renewed
without fear of data loss during extraction or monitoring. However, if
we take into account the restrictions of the Basic Access tier -- such
as the 100-tweet monthly cap, the rate limit of 1 request every 15
minutes on the main tweet retrieval endpoint, and limited access to
certain endpoints (e.g., *GET /2/tweets/search/all* is not available for
Basic Access tier users) --, then the answer is no. Even if tokens are
renewed, these tier-based restrictions tied to the app/user prevent
continuous and comprehensive data collection.

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

This criterion requires code development [[Rafael Tadeu Cardoso dos
Santos]{.underline}](mailto:rafael.cardoso@netlab.eco.ufrj.br)

**Justification:**

The *GET /2/tweets/:id* endpoint enables the retrieval of comprehensive
information about a single tweet, as identified by the provided ID ([[X,
n.d.-c]{.underline}](https://docs.x.com/x-api/posts/get-post-by-id)).

**OC5: Does the platform's API offer an endpoint for extracting data
from an individual author?**

This item verifies whether it is possible to collect data from public
posts made by a specific author, using their username or unique
identifier. The assessment should review the API documentation and test
relevant endpoints to confirm that data can be retrieved directly for an
individual author.

-   **Yes**

-   No

This criterion requires code development [[Rafael Tadeu Cardoso dos
Santos]{.underline}](mailto:rafael.cardoso@netlab.eco.ufrj.br)

**Justification:**

The *GET /2/users/:id/tweets* endpoint enables the retrieval of
comprehensive information about tweets made by a specific user, as
identified by the provided ID ([[X,
n.d.-d]{.underline}](https://docs.x.com/x-api/users/get-posts)).

**OC6: Does the platform's API provide an endpoint for extracting data
based on search terms?**

This item verifies whether public user-generated content can be
collected via individual or combined search terms, enabling the creation
of datasets of posts mentioning those terms. The assessment should test
search-related endpoints to confirm that queries using keywords return
matching public posts.

-   **Yes**

-   No

This criterion requires code development [[Rafael Tadeu Cardoso dos
Santos]{.underline}](mailto:rafael.cardoso@netlab.eco.ufrj.br)

**Justification:**

The *GET /2/tweets/search/recent* ([[X,
n.d.-i]{.underline}](https://docs.x.com/x-api/posts/search-recent-posts))
endpoint enables the retrieval of comprehensive information about tweets
published in the past seven days that match specific search terms, while
the *GET /2/tweets/search/all* ([[X,
n.d.-h]{.underline}](https://docs.x.com/x-api/posts/search-all-posts))
endpoint, available only to Pro and Enterprise API users, allows
querying historical tweets dating back to the launch of the platform.

**OC7: Does the API use locale-neutral data representations?**

This item verifies whether locale-sensitive data (e.g., timestamps,
currency, numbers) are returned in a locale-neutral format, or whether
relevant locale metadata is included when neutrality is not possible.
The assessment should review the API documentation and inspect sample
responses to confirm the presence of standardized formats or
accompanying metadata.

-   **Yes**

-   No

This criterion requires code development [[Rafael Tadeu Cardoso dos
Santos]{.underline}](mailto:rafael.cardoso@netlab.eco.ufrj.br)

**Justification:**

Based on a review of the X/Twitter API v2 documentation, the API employs
largely locale-neutral representations for non-content metadata. Its
structure and use of standardized formats ensure significant
neutrality-- for example, all timestamps (such as *created\_at*) adhere
to the ISO 8601 format and are returned in Coordinated Universal Time
(UTC) ([[X,
n.d.-k]{.underline}](https://developer.x.com/en/docs/x-ads-api/timezones)).
Similarly, the *lang* field uses ISO 639-1 language codes, and country
or regional codes follow standard ISO 3166-1 Alpha-2 conventions ([[X,
n.d.-e]{.underline}](https://developer.x.com/en/docs/x-api/v1/developer-utilities/supported-languages/api-reference/get-help-languages)).

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

**Justification:**

The X/Twitter API documentation includes a dedicated section on
migrating from API v1.1 to v2, outlining the key differences and new
features. Although no deprecation timeline is provided, it states that
v1.1 endpoints will remain functional but will no longer receive new
features or updates ([[X,
n.d.-f]{.underline}](https://docs.x.com/x-api/migrate/overview);
[[n.d.-n]{.underline}](https://developer.x.com/en/support/x-api/v2)).

**OC9: Is the platform's API documentation published in open access?**

This item verifies whether the platform makes its API documentation
openly available on the internet, without requiring registration or
login. The assessment should check whether full documentation can be
accessed freely online without requiring account creation or
authentication.

-   **Yes**

-   No

**Justification:**

The X/Twitter API documentation is publicly accessible to anyone ([[X,
n.d.-l]{.underline}](https://developer.x.com/en/docs/x-api)).

**OC10: Is the platform's API documentation clearly written and
exemplified?**

This item verifies whether the documentation for the platform's API is
clear, complete, and provides practical implementation examples. The
assessment should review the documentation to confirm the presence of
detailed explanations, structured references, and sample code or queries
that illustrate correct usage.

-   **Yes**

-   No

**Justification:**

The X/Twitter API documentation is comprehensive and includes all the
necessary information, such as account-level limitations, permissions,
detailed endpoint descriptions, and both current and upcoming features
([[X, n.d.-l]{.underline}](https://developer.x.com/en/docs/x-api)). It
also provides a well-structured migration guide from the previous
version to the current one ([[X,
n.d.-f]{.underline}](https://docs.x.com/x-api/migrate/overview)).

**OC11: Does the platform's API documentation include or link to the API
terms of use?**

This item verifies whether the documentation clearly states or links to
the terms of use governing the API and its legal aspects. The assessment
should review the documentation to confirm the presence of explicit
legal terms that define permitted use and restrictions.

-   **Yes**

-   No

**Justification:**

The X/Twitter API documentation includes an extensive set of developer
terms, collectively referred to as the "Developer Agreement and Policy"
([[X,
n.d.-b]{.underline}](https://developer.x.com/en/developer-terms/agreement-and-policy)).

**OC12: Does the platform's API documentation detail the response format
of each endpoint?**

This item verifies whether the API documentation specifies the response
format for each endpoint, including examples and potential error codes.
The assessment should review the documentation to confirm that, in all
or most cases, response structures are explicitly described and
illustrated with sample outputs.

-   **Yes**

-   No

**Justification:**

For each endpoint, the X/Twitter API documentation clearly describes the
response format, specifying the structure of the returned JSON, the
possible fields, their data types, and when they may or may not appear
([[X API Developers,
n.d.]{.underline}](https://www.postman.com/xapidevelopers/x-api-public-workspace/collection/r90eid4/x-api-v2)).

**OC13: Does the platform provide its API documentation in the official
languages of the assessed region?**

This item verifies whether the platform provides its API documentation
in the official languages of the assessed region. The assessment should
review the documentation to confirm that complete and up-to-date
versions are available in those languages.

-   Yes

-   **No**

**Justification:**

The X/Twitter API documentation is available only in English ([[X,
n.d.-l]{.underline}](https://developer.x.com/en/docs/x-api)).

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

**Justification:**

The X/Twitter API documentation clearly outlines the rate limits and
quotas for each access tier, specifying how many requests can be made,
within what time frame, and which resources or endpoints are affected
([[X,
n.d.-a]{.underline}](https://docs.x.com/x-api/getting-started/about-x-api)).

**OC15: Does the platform provide a way to label content that has been
generated with artificial intelligence?**

This item verifies whether the platform automatically flags, or allows
users to flag, AI-generated content, and whether this information is
given in the API response. The assessment should review the
documentation and test API outputs to confirm that these flags are
included in the extracted data.

-   Yes

-   **No**

This criterion requires code development [[Rafael Tadeu Cardoso dos
Santos]{.underline}](mailto:rafael.cardoso@netlab.eco.ufrj.br)

**Justification:**

X/Twitter does not allow content generated with the assistance of
artificial intelligence to be labeled. Consequently, this type of
information cannot be retrieved via the API.

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

-   Yes

-   No

-   **Not applicable**

**Justification:**

Although it could be argued that replies and quotes serve this function,
X/Twitter does not have dedicated comment features like other social
media platforms analyzed in this study.

**OC17: Can data from temporary content be extracted through the
platform's API?**

This item verifies whether the platform's API provides at least one
endpoint for collecting data from temporary publications (e.g., stories,
ephemeral messages). The assessment should test endpoints to confirm
whether this type of short-lived content can be retrieved as structured
data before it expires. This item does not apply to platforms that do
not have temporary content features.

-   **Yes**

-   No

-   Not applicable

This criterion requires code development [[Rafael Tadeu Cardoso dos
Santos]{.underline}](mailto:rafael.cardoso@netlab.eco.ufrj.br)

**Justification:**

The X/Twitter API allows the retrieval of Spaces, live audio
conversations that remain available for a limited period of time,
through specific endpoints, either by known identifiers or by keywords
([[X,
n.d.-j]{.underline}](https://docs.x.com/x-api/spaces/introduction)).

**OC18: Can historical data be extracted through the platform's API?**

This item verifies whether the API provides endpoints that allow for a
specified time range, going back more than one year from the time the
request is made, to collect public user-generated content data. The
assessment should review test endpoints to confirm that historical data
more than 12 months prior to the analysis can be retrieved.

-   **Yes**

-   No

This criterion requires code development [[Rafael Tadeu Cardoso dos
Santos]{.underline}](mailto:rafael.cardoso@netlab.eco.ufrj.br)

**Justification:**

The *GET /2/tweets/search/all* ([[X,
n.d.-h]{.underline}](https://docs.x.com/x-api/posts/search-all-posts))
endpoint allows querying historical tweets dating back to the launch of
the platform, but it is only available to Pro and Enterprise API users.

**OC19: Is the number of requests allowed by the API sufficient for
monitoring more than 10,000 publications in 24 hours?**

This item verifies whether data can be extracted without interruption
and losses through the platform's API for requests that accumulate more
than 10,000 publications in 24 hours. The assessment should test the API
to confirm that this volume of data can be collected continuously.

-   Yes

-   **No**

This criterion requires code development [[Rafael Tadeu Cardoso dos
Santos]{.underline}](mailto:rafael.cardoso@netlab.eco.ufrj.br)

**Justification:**

Although it is technically possible to monitor more than 10,000 posts in
24 hours using the X/Twitter API, the cost makes this impractical. The
Basic Access tier, priced at USD 200 per month, allows retrieval of only
15,000 posts per month, which severely restricts large-scale monitoring,
unless users opt for the Pro Access tier, which costs USD 5,000 per
month ([[X,
n.d.-a]{.underline}](https://docs.x.com/x-api/getting-started/about-x-api)).

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

-   **Yes**

-   No

This criterion requires code development [[Rafael Tadeu Cardoso dos
Santos]{.underline}](mailto:rafael.cardoso@netlab.eco.ufrj.br)

**Justification:**

Excluding the seven-day limitation of the GET /2/tweets/search/recent
endpoint ([[X,
n.d.-i]{.underline}](https://docs.x.com/x-api/posts/search-recent-posts)),
data acquisitions using the X/Twitter API are consistently reproducible
over time.

**OC21: Is the data returned by the platform's API consistent with the
parameters and filters used in the request?**

This item verifies whether the data extracted through the API accurately
reflects the parameters and filters specified in the request. The
assessment should conduct repeated test queries to confirm the
consistency of results or ground the response based on recent (less than
2 years) experiments published in peer-reviewed journals.

-   **Yes**

-   No

This criterion requires code development [[Rafael Tadeu Cardoso dos
Santos]{.underline}](mailto:rafael.cardoso@netlab.eco.ufrj.br)

**Justification:**

The platform returns data which matches the parameters and filters
applied.

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

This criterion requires code development [[Rafael Tadeu Cardoso dos
Santos]{.underline}](mailto:rafael.cardoso@netlab.eco.ufrj.br)

**Justification:**

The data extracted through the platform's API reflects what is displayed
on the user interface at the moment it is collected, meaning that key
elements such as authorship, full content, interaction metrics, and
referenced content are consistent with what users see on the interface.

**OC23: Does the platform's API allow for filtering data based on
publisher location?**

This item verifies whether the API supports applying location-based
filters to data extraction. The assessment should test the endpoint for
the main content type to confirm that data on public posts can be
filtered by publisher location.

-   **Yes**

-   No

This criterion requires code development [[Rafael Tadeu Cardoso dos
Santos]{.underline}](mailto:rafael.cardoso@netlab.eco.ufrj.br)

**Justification:**

The X/Twitter API v2 documentation indicates that it is possible to
filter data by publisher location using the profile\_region field.
However, this filter is not available to users or developers on the
Basic Access tier. Therefore, we were unable to test or validate this
functionality ([[X,
n.d.-g]{.underline}](https://docs.x.com/x-api/enterprise-gnip-2.0/fundamentals/rules-filtering)).

**OC24: Does the platform's API allow for filtering data based on
content language?**

This item verifies whether the API allows for applying language-based
filters to data extraction. The assessment should test the endpoint for
the main content type to confirm that public post data can be filtered
by content language.

-   **Yes**

-   No

This criterion requires code development [[Rafael Tadeu Cardoso dos
Santos]{.underline}](mailto:rafael.cardoso@netlab.eco.ufrj.br)

**Justification:**

The *GET /2/tweets/search/recent* ([[X,
n.d.-i]{.underline}](https://docs.x.com/x-api/posts/search-recent-posts))
and *GET /2/tweets/search/all* ([[X,
n.d.-h]{.underline}](https://docs.x.com/x-api/posts/search-all-posts))
endpoints enable filtering of tweets according to content language
through the use of the *lang* parameter.

**OC25: Does the platform's API allow for filtering data by specific
time periods?**

This item verifies whether the API allows applying temporal filters to
data extraction. The assessment should test the endpoint for the main
content type to confirm that public post data can be filtered by custom
time ranges.

-   **Yes**

-   No

This criterion requires code development [[Rafael Tadeu Cardoso dos
Santos]{.underline}](mailto:rafael.cardoso@netlab.eco.ufrj.br)

**Justification:**

The *GET /2/tweets/search/recent* ([[X,
n.d.-i]{.underline}](https://docs.x.com/x-api/posts/search-recent-posts)),
though limited to the last seven days, and *GET /2/tweets/search/all*
([[X,
n.d.-h]{.underline}](https://docs.x.com/x-api/posts/search-all-posts))
endpoints allow filtering of tweets based on specific timeframes.

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

This criterion requires code development [[Rafael Tadeu Cardoso dos
Santos]{.underline}](mailto:rafael.cardoso@netlab.eco.ufrj.br)

**Justification:**

In our tests, we found that the delay between content appearing on the
user interface and being accessible through the API was minimal,
typically less than one hour.

REFERENCES
----------

Dongo, I., Cadinale, Y., Aguilera, A., Martínez, F., Quintero, Y., &
Barrios, S. (2020, November). Web scraping versus twitter API: a
comparison for a credibility analysis. In *Proceedings of the 22nd
International conference on information integration and web-based
applications & services* (pp. 263-273).
[[https://doi.org/10.1145/3428757.3429104]{.underline}](https://doi.org/10.1145/3428757.3429104)

Johnson, R. (2018, April 26). *Twitter developer platform and user
privacy*. Twitter Developer Platform Blog.
[[https://blog.x.com/developer/en\_us/topics/tools/2018/twitter-developer-platform-and-user-privacy]{.underline}](https://blog.x.com/developer/en_us/topics/tools/2018/twitter-developer-platform-and-user-privacy)

Mimizuka, K., Brown, M. A., Yang, K. C., & Lukito, J. (2025).
Post-Post-API Age: Studying Digital Platforms in Scant Data Access
Times. *arXiv preprint arXiv:2505.09877*.
[[https://doi.org/10.48550/arXiv.2505.09877]{.underline}](https://doi.org/10.48550/arXiv.2505.09877)

Nóbrega, L. (2023, February 2). *Twitter encerra acesso gratuito à API a
partir do dia 9*. desinformante.
[[https://desinformante.com.br/twitter-api/]{.underline}](https://desinformante.com.br/twitter-api/)

X. (n.d.-a). *About the X API*. X Developer Platform.
[[https://docs.x.com/x-api/getting-started/about-x-api]{.underline}](https://docs.x.com/x-api/getting-started/about-x-api)

X. (n.d.-b). *Developer Agreement and Policy*. X Developer Platform.
[[https://developer.x.com/en/developer-terms/agreement-and-policy]{.underline}](https://developer.x.com/en/developer-terms/agreement-and-policy)

X. (n.d.-c). *Get Post by ID*. X Developer Platform.
[[https://docs.x.com/x-api/posts/get-post-by-id]{.underline}](https://docs.x.com/x-api/posts/get-post-by-id)

X. (n.d.-d). *Get Posts*. X Developer Platform.
[[https://docs.x.com/x-api/users/get-posts]{.underline}](https://docs.x.com/x-api/users/get-posts)

X. (n.d.-e). *Get Twitter supported languages*. X Developer Platform.
[[https://developer.x.com/en/docs/x-api/v1/developer-utilities/supported-languages/api-reference/get-help-languages]{.underline}](https://developer.x.com/en/docs/x-api/v1/developer-utilities/supported-languages/api-reference/get-help-languages)

X. (n.d.-f). *Migration Guide: Overview*. X Developer Platform.
[[https://docs.x.com/x-api/migrate/overview]{.underline}](https://docs.x.com/x-api/migrate/overview)

X. (n.d.-g). *Rules and filtering: Enterprise*. X Developer Platform.
[[https://docs.x.com/x-api/enterprise-gnip-2.0/fundamentals/rules-filtering]{.underline}](https://docs.x.com/x-api/enterprise-gnip-2.0/fundamentals/rules-filtering)

X. (n.d.-h). *Search all Posts*. X Developer Platform.
[[https://docs.x.com/x-api/posts/search-all-posts]{.underline}](https://docs.x.com/x-api/posts/search-all-posts)

X. (n.d.-i). *Search recent Posts*. X Developer Platform.
[[https://docs.x.com/x-api/posts/search-recent-posts]{.underline}](https://docs.x.com/x-api/posts/search-recent-posts)

X. (n.d.-j). *Spaces: Introduction*. X Developer Platform.
[[https://docs.x.com/x-api/spaces/introduction]{.underline}](https://docs.x.com/x-api/spaces/introduction)

X. (n.d.-k). *Timezones*. X Developer Platform.
[[https://developer.x.com/en/docs/x-ads-api/timezones]{.underline}](https://developer.x.com/en/docs/x-ads-api/timezones)

X. (n.d.-l). *X API*. X Developer Platform.
[[https://developer.x.com/en/docs/x-api]{.underline}](https://developer.x.com/en/docs/x-api)

X. (n.d.-m). *X API v2 data dictionary*. X Developer Platform.
[[https://docs.x.com/x-api/fundamentals/data-dictionary]{.underline}](https://docs.x.com/x-api/fundamentals/data-dictionary)

X. (n.d.-n). *X API v2 Support*. X Developer Platform.
[[https://developer.x.com/en/support/x-api/v2]{.underline}](https://developer.x.com/en/support/x-api/v2)

X API Developers. (n.d.). X API v2 \[Postman Collection\]. Postman.
[[https://www.postman.com/xapidevelopers/x-api-public-workspace/collection/r90eid4/x-api-v2]{.underline}](https://www.postman.com/xapidevelopers/x-api-public-workspace/collection/r90eid4/x-api-v2)

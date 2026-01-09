

# **Items**

## SPECIAL CRITERIA

**SC1: Does the platform provide an API to access its ad repository and extract data on advertising content?** \- weight 0.50  
This item verifies whether the platform provides an ad repository API with at least one endpoint for programmatically extracting advertising data. Full availability is confirmed when the API returns information on ads across all categories. The assessment should confirm that the endpoint allows the retrieval and storage of ad data without requiring privileged or internal access beyond standard developer registration.

- Yes, with full availability  
- Yes, with partial availability   
- **No**

The platform provides a Commercial Content API to access its ad repository and extract data. However, the functionality of the API could not be confirmed at the time of this assessment as access was not obtained despite multiple requests ([TikTok, n.d.](https://developers.tiktok.com/products/commercial-content-api)).

**SC2: Does the platform provide a graphical user interface to its ad repository for extracting advertising content data?** \- weight 0.30  
This item verifies whether the platform provides a graphical user interface (GUI) for extracting ad data in a structured format for external use. Full availability is considered granted when the GUI delivers information on ads across all categories. The assessment should confirm the availability of an official browser-based tool that allows users not only to view ad content but also to export its data.

- Yes, with full availability  
- **Yes, with partial availability**   
- No

TikTok provides access to a Commercial Content Library for all EU countries. This is a GUI for its repository of all ads that are running on TikTok including ads that are not presently active or paused by the advertisers ([TikTok, n.d.](https://library.tiktok.com/)) However there is no export functionality.

**SC3: Can data from both active and inactive ads be extracted?** \- weight 0.20  
This item verifies whether the platform allows the extraction of ad data through either the GUI or the API, from at least one day after publication to at least one year prior. Full availability is confirmed when both active and inactive ad data are delivered across all ad categories. The assessment should test the interface and endpoints to confirm whether both active and inactive ads can be retrieved.

- Yes, with full availability  
- Yes, with partial availability  
- **No**

Although ads which are not currently active are visible on the Commercial Content Library, no ads can be extracted through the GUI. Moreover, the functionality of the API could not be confirmed at the time of this assessment as access was not obtained despite multiple requests.

## OTHER CRITERIA

### ACCESSIBILITY

*Accessibility measures how easily data can be located, retrieved, understood and used.*

**OC1: Does the platform provide a GUI for accessing and visualizing its ad repository?\***  
This item verifies whether the platform provides a GUI for accessing and viewing ads in its ad repository. Full access is confirmed when the GUI provides information on ads across all categories and publication statuses, including both active and inactive ads. The assessment should confirm the availability of an official browser-based tool that allows users to search, access, and view ad content.

- **Yes, with full availability**  
- Yes, with partial availability   
- No

**OC2: Is access to the platform’s ad repository free of charge?**  
This item verifies whether the ad repository API or GUI is free of charge, since even modest fees can create barriers or force researchers in low-resourced settings to narrow the scope of their work. The assessment should verify the platform’s documentation and pricing policies to confirm that no fees are applied for access to the ad repository.

- **Free API access**  
- **Free GUI access**  
- No

**OC3: Can the requested data be extracted directly from the ad repository response?**  
This item verifies whether the platform’s ad repository returns structured data on ad content and authorship directly in the response, rather than providing a link that redirects to the data. Audiovisual media files and data (e.g., images, videos, and audio) should not be considered when assessing this item. The assessment should examine sample data responses from both the ad repository GUI and API to confirm that the requested public data is included in the returned payload.

- Yes, through the GUI  
- Yes, through the API  
- **No**

The requested data cannot be extracted directly from the ad repository response as there is no way to extract data from the GUI. The API provides a way to extract data, however this has not been confirmed as access was not obtained at the time of this assessment.

**OC4: Does the platform’s ad repository API provide a form of authentication that allows for renewal without the risk of data loss?\***  
This item verifies whether the tokens provided for API use can be renewed without the risk of data loss, ensuring continuity and integrity of data access and monitoring. The assessment should check the platform’s documentation or directly observe the authentication and renewal process to confirm that token updates do not interrupt or compromise data access.

- **Yes**  
- No

The TikTok Commercial Content API supports renewable authentication via short-lived access tokens ([TikTok, n.d.](https://developers.tiktok.com/doc/commercial-content-api-query-ads?enter_method=left_navigation)).

**OC5: Can data from an individual ad be retrieved from the platform?**  
This item verifies whether it is possible to retrieve data from a specific advertisement on the ad repository using a unique identifier, rather than relying on search terms or other parameters and filters. The assessment should review the ad repository documentation and test available features to confirm that an individual ad can be retrieved directly by its unique identifier.

- Yes, through the GUI  
- Yes, through the API  
- **No**

Data from an individual ad can be retrieved from the platform according to the API documentation ([TikTok, n.d.](https://developers.tiktok.com/doc/commercial-content-api-query-ads?enter_method=left_navigation)); however this has not been confirmed due to lack of access to the API at the time of this assessment. There is no export functionality on the GUI, though this information can be queried and viewed online.

**OC6: Can data from ads served by a specific advertiser be retrieved from the platform?**  
This item verifies whether it is possible to retrieve data from ads run by a specific advertiser, via their username or unique identifier. The assessment should review the ad repository documentation and test any available feature to retrieve data from an individual advertiser.

- Yes, through the GUI  
- Yes, through the API  
- **No**

Data from ads served by a specific advertiser can be retrieved from the platform according to the API documentation by using the “advertiser\_business\_ids” filter ([TikTok, n.d.](https://developers.tiktok.com/doc/commercial-content-api-query-ads?enter_method=left_navigation)); however this has not been confirmed due to lack of access to the API at the time of this assessment. There is no export functionality on the GUI, though this information can be queried and viewed online.

**OC7: Can ad data be retrieved from the platform using search terms?**  
This item verifies whether ad data can be retrieved through search terms, enabling the creation of datasets based on those queries. The assessment should test search-related features to confirm that it accepts search queries using keywords.

- Yes, through the GUI  
- Yes, through the API  
- **No**

Data from ads filtered using search terms can be retrieved from the platform according to the API documentation by using the “search\_term” filter ([TikTok, n.d.](https://developers.tiktok.com/doc/commercial-content-api-query-ads?enter_method=left_navigation)); however this has not been confirmed due to lack of access to the API at the time of this assessment. There is no export functionality on the GUI, though this information can be queried and viewed online.

**OC8: Does the platform use locale-neutral data representations?**  
This item verifies whether locale-sensitive data (e.g., timestamps, currency, numbers) are provided in a locale-neutral format, or, if that is not possible, whether relevant locale metadata is included. The assessment should review the ad repository documentation and inspect sample responses to confirm the presence of standardized formats or accompanying metadata.

- **Yes, through the GUI**  
- **Yes, through the API**  
- No

Based on a review of the API documentation, this API employs locale-neutral representation; however this has not been confirmed due to lack of access to the API at the time of this assessment. The GUI also provides dates and country information in a locale-neutral manner. 

### COMPLETENESS

*Completeness refers to how closely the data reflects the dimensions of what it represents (in breadth, depth and scope).*

**OC9: Does the platform provide data that allows the identification of advertisers who ran ads?**  
This item verifies whether the platform discloses information on the advertisers responsible for the identified ads. The assessment should confirm whether the advertiser’s page name, URL, and unique identifier can be retrieved.

- **Yes, through the GUI**  
- Yes, through the API  
- No

The GUI provides partial data: it provides the advertiser’s name; however no unique identifier is visible and the URL is not always available: when it is, it is clickable and not immediately obvious to the user. No data can be extracted from the platform via the GUI. 

According to the documentation, the API should provide data regarding the business name and business id as well as their profile URL. However, this has not been confirmed due to lack of access to the API at the time of this assessment.

**OC10: Does the platform provide data on the funders who paid for ads?**  
This item verifies whether the platform provides data on the individuals or organizations that paid for the identified ads. The assessment should confirm whether any sponsor information is retrievable.

- **Yes, through the GUI**  
- Yes, through the API  
- No

The GUI provides the funders’ name; however no data can be extracted from the platform via the GUI.

According to the documentation, the API should provide data regarding an ad’s funder via the “advertiser.paid\_for\_by” field. However, this has not been confirmed due to lack of access to the API at the time of this assessment.

**OC11: Does the platform provide data on the period during which ads were served?**  
This item verifies whether the platform provides data on the days on which the identified ads ran. The assessment should review the extracted ad data to confirm that it includes start and end dates (or equivalent temporal markers) indicating the period of activity.

- **Yes, through the GUI**  
- Yes, through the API  
- No

The GUI provides data on the period during which ads were served; however no data can be extracted from the platform via the GUI. 

According to the documentation, the API should provide data regarding when an ad was served via the “ad.first\_shown\_date” and the  “ad.last\_shown\_date” fields. However, this has not been confirmed due to lack of access to the API at the time of this assessment.

**OC12: Does the platform provide data on user engagement with ads?**  
This item verifies whether the platform provides data on the total number of user interactions with ads (e.g., likes, comments, shares, clicks). The assessment should review the extracted ad data to confirm that engagement metrics are available and clearly linked to each ad.

- **Yes, through the GUI**  
- Yes, through the API  
- No

The GUI provides limited data on user engagement: it provides how many unique users have seen an ad (however the ranges are quite broad, including anywhere from “0-1k”) as well as the “Target audience size” which is “an estimate of how many users meet the targeting and ad placement criteria that advertisers select when creating their ad campaign”. Moreover, no data can be extracted from the platform via the GUI. 

According to the documentation, the API should provide data regarding the ad reach via the “unique\_users\_seen” field. However, this has not been confirmed due to lack of access to the API at the time of this assessment.

**OC13: Does the platform indicate whether ads were placed by verified or unverified advertisers?**  
This item verifies whether the platform clearly indicates whether advertisers were verified at the time their ads were served. The assessment should review ad records to confirm that a verification status field is present.

- **Yes, through the GUI**  
- Yes, through the API  
- No

This information is visible on the GUI as a blue tick next to the advertiser’s name and logo. However when an advertiser’s TikTok profile is not linked, this information is not available, such as when an advertiser is simply named and no link is provided. This information cannot be extracted from the GUI.

According to the API documentation, the API does not provide data regarding whether an advertiser is verified or not. 

### COMPLIANCE

*Compliance refers to how data adheres to standards, conventions and regulations in a given context. It ensures that data is formatted and structured in the way it ought to be, according to external or internal rules.*

**OC14: Does the platform flag ads that were removed due to violations of its guidelines or relevant legislation?**  
This item verifies whether the platform indicates when an ad has been moderated. At a minimum, the platform should provide the reason for removal and the date. The assessment should review ad records to confirm that moderated ads are flagged and that the corresponding moderation details are clearly documented.

- **Yes, through the GUI**  
- Yes, through the API  
- No

According to the documentation, on the GUI “Note: Some ads may display a label that indicates it was removed because of a violation of our terms.” These ads are not viewable, but some details may be visible, “such as the number of unique users who have seen the ad at least once, or the targeting summary.” ([TikTok, n.d.](https://support.tiktok.com/en/account-and-privacy/personalized-ads-and-data/commercial-content-library)). This information cannot be extracted from the GUI.

According to the documentation, the API provides data regarding an ad’s moderation or rejections via the “rejection\_info” field which provides details such as “reasons” (the reason that an ad has been rejected), “affected\_countries” (the affected regions where the listed rejection reasons may apply), “reporting\_source” (the reporting or detection source, where applicable), and “automated\_notice” (whether the moderation decision relied on automated measures). However, this has not been confirmed due to lack of access to the API at the time of this assessment.

**OC15: Does the platform indicate whether ad content was generated using artificial intelligence?**  
This item verifies whether the platform flags ads in which AI was involved in generating the content. The assessment should review ad records to confirm the presence of a field or label indicating the use of AI in ad production.

- Yes, through the GUI  
- Yes, through the API  
- **No**

**OC16: Is the platform’s ad repository documentation published in open access?**  
This item verifies whether the platform makes its ad repository documentation openly available on the internet, without requiring user registration or login. The assessment should attempt to access the documentation directly to confirm that it is fully available without authentication barriers.

- **Yes, the API documentation**  
- **Yes, the GUI documentation**  
- No

The API documentation ([TikTok, n.d.](https://developers.tiktok.com/doc/commercial-content-api-getting-started?enter_method=left_navigation)) and the GUI documentation ([TikTok, n.d.](https://support.tiktok.com/en/account-and-privacy/personalized-ads-and-data/commercial-content-library)) are openly available without requiring user registration or login information. 

**OC17: Is the platform’s ad repository documentation clearly written and exemplified?**  
This item verifies whether the documentation for the platform’s ad repository is clear, complete, and provides practical implementation examples. The assessment should review the documentation to confirm the presence of detailed explanations, structured references, and sample queries or outputs illustrating correct use.

- **Yes, the API documentation**  
- **Yes, the GUI documentation**  
- No

The API documentation ([TikTok, n.d.](https://developers.tiktok.com/doc/commercial-content-api-getting-started?enter_method=left_navigation)) and the GUI documentation ([TikTok, n.d.](https://support.tiktok.com/en/account-and-privacy/personalized-ads-and-data/commercial-content-library)) are clearly written and exemplified.

**OC18: Does the platform’s ad repository documentation include or link to its terms of use?**  
This item verifies whether the documentation clearly and unambiguously states or refers to the terms for using the ad repository and its associated legal aspects. The assessment should review the documentation to confirm that explicit terms or references are provided and accessible.

- **Yes, the API documentation**  
- Yes, the GUI documentation  
- No

The API documentation provides an overarching link to “developer guidelines” linking to the developer Terms of Service ([TikTok, n.d.](https://developers.tiktok.com/doc/our-guidelines-developer-guidelines?enter_method=left_navigation)). However the GUI documentation does not.

**OC19: Does the platform provide its ad repository documentation in the official languages of the assessed region?**  
This item verifies whether the platform provides its ad repository documentation in the official languages of the region being assessed. The assessment should review the documentation to confirm that complete and up-to-date versions are available in those languages.

- Yes, the API documentation  
- Yes, the GUI documentation  
- **No**

The GUI documentation is not available in all 24 official languages of the EU, it is available in 23 out of 24: there is no Maltese ([TikTok, n.d.](https://support.tiktok.com/en/account-and-privacy/personalized-ads-and-data/commercial-content-library)). 

The API documentation is only available in English, missing 23 languages ([TikTok, n.d.](https://developers.tiktok.com/doc/commercial-content-api-getting-started?enter_method=left_navigation)).

**OC20: Does the platform implement a proper deprecation strategy to avoid breaking client applications while rolling out major changes in the API?\***   
This item verifies whether the platform’s documentation describes a deprecation strategy with a grace period before removing features. The assessment should review changelogs to confirm that deprecated features are listed with deprecation and removal dates and include migration instructions. This item applies only to breaking changes that require client updates, such as endpoint modifications, authentication updates, or the removal of features.

- **Yes**  
- No or not applicable

The Commercial API is documented in the API documentation changelog [(TikTok, n.d.](https://developers.tiktok.com/doc/changelog?enter_method=left_navigation)).

**OC21: Does the platform’s ad repository API documentation detail the response format of each endpoint?\***  
This item verifies whether the platform’s ad repository API documentation specifies the format of each possible response, including examples and potential errors. The assessment should review the documentation to confirm that response structures are described and illustrated with sample outputs.

- **Yes**  
- No or not applicable

**OC22: Does the platform’s ad repository API documentation detail the quota or rate limits applicable to each available endpoint?\***  
This item verifies whether the platform’s ad repository API documentation specifies the limits for each endpoint, including any variations based on authentication level or endpoint type. Rate and quota limits define the maximum number of requests allowed within a given period (e.g., 1,000 requests per hour). The assessment should review the documentation to confirm that request caps (rate limits) and overall usage restrictions (quotas) are clearly stated.

- Yes  
- **No or not applicable**

The quote or rate limits are not detailed in the API documentation.

### CONSISTENCY

*This dimension tracks whether the data always presents the same values, the same format in every occurrence and if it is compatible with the previous data.*

**OC23: Does the data retrieved by the API reflect what is displayed on the platform’s ad repository GUI?\***  
This item verifies whether the data returned by the platform’s ad repository API corresponds to the information displayed on its GUI in all its levels of detail. It should be possible to identify in the API response information such as authorship, complete content, and other serving information (e.g., amount spent, impressions reached). The assessment should compare API responses with the GUI to confirm that at least the following elements are consistent: authorship, full content, and serving information (e.g., spending, impressions).

- Yes  
- **No or not applicable**

This cannot be verified due to lack of access to the API at the time of this assessment.

**OC24: Are the results returned by the platform consistently reproducible?**  
This item verifies whether data accessed and extracted via the platform’s ad repository at a given time is consistent with other collections performed similarly, including cases where content was deleted in the interim. The assessment should perform repeated queries to confirm the reproducibility of results.

- **Yes, through the GUI**  
- Yes, through the API  
- No

This cannot be verified for the API due to lack of access at the time of this assessment.

**OC25: Is the data returned by the platform consistent with the parameters and filters used in the request?**  
This item verifies whether the data retrieved through the ad repository accurately reflects the parameters and filters specified at the time of the request. The assessment should run test queries with different filters to confirm that results consistently match the requested conditions.

- **Yes, through the GUI**  
- Yes, through the API  
- No

This cannot be verified for the API due to lack of access at the time of this assessment.

### RELEVANCE

*Relevance evaluates how helpful the data is and how applicable for use it is, also considering future applications. This dimension also evaluates the extent to which the content and coverage of data meet the user’s needs.*

**OC26: Does the platform allow the use of temporal filters to retrieve data on ads?**  
This item verifies whether the ad repository allows filtering data by the time period in which the ads were served. The assessment should test queries with temporal filters to confirm that results accurately reflect the specified date ranges.

- **Yes, through the GUI**  
- Yes, through the API  
- No

The GUI allows filtering data by the time period in which the ads were served; however no data can be extracted from the platform via the GUI. 

According to the documentation, the API should provide data regarding when an ad was served via the “ad.first\_shown\_date” and the  “ad.last\_shown\_date” fields. However, this has not been confirmed due to lack of access to the API at the time of this assessment.

**OC27: Does the platform allow filtering advertising data by ad category?**

This item verifies whether the ad repository allows filtering data by any categories assigned at the time of ad creation. The assessment should run test queries with category filters to confirm that results align with the selected classifications.

- Yes, through the GUI  
- Yes, through the API  
- **No or not applicable**

Neither the GUI nor the API allow filtering by ad category.

**OC28: Does the platform allow filtering advertising data by geographic location?**  
This item assesses whether the ad repository allows filtering data by one or more subnational geographic locations where the ads were served. The assessment should test queries with location filters to confirm that results match the specified areas.

- **Yes, through the GUI**  
- Yes, through the API  
- No

The GUI allows filtering data by geographical location; however no data can be extracted from the platform via the GUI. 

According to the documentation, the API should provide geographical location via the “country\_code” field. However, this has not been confirmed due to lack of access to the API at the time of this assessment.

### ACCURACY

*Accuracy assesses how closely data reflects real-world phenomena, measuring the correctness of its representation of reality.*

**OC29: Does the platform provide age and gender data on the audiences of ads?**  
This item verifies whether the platform provides data on the age and gender of audiences reached. The assessment should review the ad records to confirm that these breakdowns are available and consistently reported.

- **Yes, through the GUI**  
- Yes, through the API  
- No

The GUI provides data on the age and gender of audiences reached; however no data can be extracted from the platform via the GUI. 

According to the documentation, the API should provide geographical location via the “targeting\_info” field which provides information on gender and age. However, this has not been confirmed due to lack of access to the API at the time of this assessment.

**OC30: Does the platform provide subnational geographic data on the audience reached by ads?**  
This item verifies whether the platform provides data on the subnational geographic location of audiences reached. The assessment should review the ad records to confirm that such location breakdowns are available and consistently reported.

- Yes, through the GUI  
- Yes, through the API  
- **No**

**OC31: Does the platform include data on audience targeting criteria defined by advertisers?**  
This item verifies whether the platform provides data on audience targeting criteria defined by the advertiser when publishing ads (e.g., demographic and geographic segments, as well as interests, attitudes, behaviors, and keywords). The assessment should review ad records to confirm that these targeting parameters are available and consistently reported.

- **Yes, through the GUI**  
- Yes, through the API  
- No

The GUI provides information about additional targeting criteria such as being part of a specific “audience” specified by the advertiser, sharing a specific “interest”, having had specific “video interactions” or “creator interactions”.

According to the documentation, the API should provide targeting criteria defined by advertisers via the “targeting\_info” field which provides information on whether a user is part of an audience list uploaded by the advertiser, whether a user has interacted with a video from a category provided by the advertiser, whether a user followed or viewed creators from a specified category or whether the user is grouped into a list of interests specified by the advertiser. However, this has not been confirmed due to lack of access to the API at the time of this assessment.

**OC32: Does the platform provide granular volume ranges for ad impressions?**  
This item verifies whether the ad repository provides impression values for ads, using ranges that closely approximate the actual numbers. Intervals should be no larger than 10% of the upper bound of the value range they represent. For example, values up to 1,000 impressions should be displayed in intervals no larger than 100; between 1,000 and 10,000 in intervals no larger than 1,000; between 10,000 and 100,000 in intervals no larger than 10,000; between 100,000 and 1 million or above, in intervals no larger than 100,000. The assessment should measure whether the reported intervals remain within this threshold across the different value ranges using the platform’s documentation or available data interfaces.

- Yes, through the GUI  
- Yes, through the API  
- **No**

The GUI does not provide granular volume ranges for ad impressions. The ranges observed on the GUI can go from “0-1K”, “10k-100k” and “300K-400K”.

This information is not available in the API documentation and this cannot be verified through the API due to lack of access at the time of this assessment.

**OC33: Does the platform provide granular investment ranges for ad spending?**  
This item verifies whether the ad repository provides spending values for ads, using ranges that closely approximate the actual amounts. Intervals should be no larger than 10% of the upper bound of the value range they represent. For example, values up to $100 should be displayed in intervals no larger than $10; between $100 and $1,000 in intervals no larger than $100; and between $1,000 and $10,000 in intervals no larger than $1,000. The assessment should measure whether the reported intervals remain within this threshold across the different value ranges using the platform’s documentation or available data interfaces.

- Yes, through the GUI  
- Yes, through the API  
- **No**

No advertising expenditure information is provided through either the GUI or the API.


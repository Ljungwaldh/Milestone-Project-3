# Mad Libz - Testing Details

## Automated Testing

### Validation Services
The following validation services and linter were used to check the validity of the website code.

- [W3C Markup Validation]( https://validator.w3.org/) was used to validate HTML.
	- No issues were found when validating via URI’s. Validating via direct input would’ve not worked since the validator does not register Jinja syntax

- [W3C CSS validation](https://jigsaw.w3.org/css-validator/) was used to validate CSS.
	- Came across a number of issues that were related to styles that were not recognised by the validator. These styles came from css code I took from Start Bootstrap themes and snippets - majority of these relating to styles for different browsers. Below are visuals of the errors/warnings the validator came across:
(insert images of CSS errors/warnings)
- These were fixed by cleaning up the CSS code, removing styles that caused errors/warnings.


- [PEP8 validation](http://pep8online.com/) was used to validate the Python code.
	- Only error found was code in my register function, where I had stated ‘if user == None’, when the right syntax in this case would be ‘ if user is None’. Fixed this promptly after the validator notified me of it

## User Stories Testing

The following section goes through each of the user stories from the UX section of [README.md](README.md)

1. As a new visitor to the website, I want it to be very clear as to what the purpose of the website is
	- A new website visitor lands on the no-login landing page, with a clear logo text and slogan, followed by a Learn More button. This button helps to relocate the user further down the page to read more about what Mad Libs are, how the website works, and how they can get started. This is finished off with two buttons at the bottom that can help prompt the user to getting starting, either by signing up or by logging in

2. As a new user to the mad lib concept, I want information about this presented early and clearly during the experience
	- With the same reasoning as User Story 1, information on what Mad Libs are is presented early to new visitors in the information section of the landing page

3. As a new user to the website, I want to be able to get started quickly in creating my own mad lib
	- While a login system does compromise efficiency for users to start creating mad lib records, the added bit of security is a relatively quick process, and once logged in, the is a button visible immediately to direct users towards creating a mad lib via the ‘Create Mad Lib’ button

4. As a new user to the website, I want to be able to navigate myself easily to different parts of the website
    - A clear navigation bar that is sticky is present on every page of the website to ensure users are never lost. The options change dynamically depending on if users are logged in or not so that they have relevant locations available at hand
    - Each page presents a clear button(s) that can also help steer users towards relevant locations in the website to give greater ease for users navigating themselves

5. As a new user to the website, I want to be able to easily see previously generated mad lib entries
	- If a user is logged in, they can easily access all created mad lib records via the navigation bar item ‘View All Mad Libz’
	- User can also directly see the mad lib they have created directly after it has been generated
	- In the same results page where the generated new mad lib is displayed, one of the option buttons available is to ‘View All Mad Libz’ to help guide users to what could be a natural next step in the user journey

6. As a new user/returning to the website, I want to be able to get in touch with the site owner to suggest new themes for the mad lib generator
	- A simple footer is provided on each page, where information about who developed the website is presented, a contact email address as well as social media links that give alternative channels for users to reach out to the website developer to give feedback/suggestions

7. As a new/returning user to the website, I want to be able to not only read my mad lib entries, but to also be able to edit and delete these if I so please
	- As soon as a user has created a mad lib, one of the buttons presented below the entry is ‘Delete’, placed here in case the user is instantly dissatisfied with the mad lib created
	- In the easily accessible ‘View All Mad Libz’ page buttons are made available on mad lib entries the user has created themselves, these buttons being ‘Edit’ and ‘Delete’

8. As a new/returning user, I want to be the only one who can edit and delete my mad lib entries through appropriate user authentication
	- As stated in User Story 7, a user can only edit/delete mad lib entries they have created themselves. User session logic has been implemented so that it makes it impossible for a user to access any page/function that relates to a mad lib they didn’t create. In this instance, the invalid user is redirected to the home page with the message appearing ‘Error: Sorry, invalid user’

## Manual Testing

Below is a comprehensive procedure describing the testing done on the website in order to confirm that all parts of the website work as they should

### Testing on Desktop 
I did this testing across Microsoft Edge, Google Chrome, Firefox and Safari web browsers. Testing was initially done on Google Chrome, followed by the other browsers to check deviations from Chrome 

#### Consistent Features on all pages

1. Navbar (not logged in)
- Clicked on logo, ended up on landing page, even coming from Log In and Sign Up pages
- Clicked on Log In, ended up onLog In, even coming from the landing page and Sign Up pages
- Clicked on Sign Up, ended up on the Sign Up page, even coming from Log In and the landing page pages
- Hovered over navbar links, checked that hover effect works
2. Navbar (logged in)
- Clicked on logo, ended up on home page, even coming from other pages available
- Clicked on Home, ended up on home page, even coming from other pages available
- Clicked on Create Mad Lib, ended up on Create page, even coming from other pages available
- Clicked on View All Mad Libz, ended up on Library page, even coming from other pages available
- Clicked on Logout, redirected to landing page for visitors not logged in

3. Footer
- Clicked on every social media icons, redirects me correctly the the right social media websites
- Hovered over icons to confirm hover effects are working

#### Landing page (not logged in)
1. Hero image
- Checked to see if it renders properly and the image is clear
- Confirmed that heading and subheading is easy to read
- Checked that the ‘Learn More’ button hover effect was working, plus tested clicking on it to confirm that it scrolls the user down the page to the beginning of the information section

2. Information section
- Checked to see if the images rendered properly and can be clearly seen
- Checked the information text on each of the three subsections in the information section to confirm readability
- Checked to see of the ‘Log In’ and ‘Sign Up’ buttons at the end of the section work

#### Login In page
1. Checked to see if clicking the ‘Log In’ button any input in text input fields would return the popup stating that the input(s) are required. Subsequently only filled out one of the inputs and tried to log in in order to test prompt for making sure both input fields are filled in
2. Tried logging in with an existing username but wrong password to confirm error message that appears as a result is working
4. Attempted to log in with both a username and password that don’t exist
	- This produced an error page, as no logic was in place to account for log in attempts where the username typed in doesn’t exist. This was fixed by applying an ‘if username is None’ check in the python logic right after the function gets the username from the form and from the database.
5. Logged in with valid username and password and I am redirected to the home page successfully, along with a message appearing under the home page header notifying me of this
6. Tested character limit for username (being 40) and for password (being 15), both these restrictions working

#### Sign Up page
1. Repeated the same process as i did for the Log In page in terms of testing character limit and trying to submit the form with filling in one or both input
2. Tried using an existing user’s username to create a new user, and correctly received the message feedback that the user already exists
3. Successful registration leads to the ‘Log In’ page with the ‘New user successfully created’ message appearing as expected

#### Home page
1. Checked to see that images rendered well and clearly on the page
2. Checked to see if hover effects works on the buttons
3. Checked to see that the buttons redirect me to the right locations
4. Coming from the Log In page after logging in successfully, I click the back button to ensure that I don’t land back on the Log In page but rather redirect/stay on the Home page

#### Create page
1. Checked to see that that the image renders clearly into the page
2. Checked to see that message pops up when I try to click the ‘Next button’ without selecting a theme from the select dropdown menu
3. Picked every option in the dropdown menu and clicked ‘Next’ to check that it renders the appropriate input fields based on the theme selected

#### Insert Words page
1. Tried submitting the form via the ‘Generate Mad Lib’ button to test input validation (that these need to be filled in)
2. Tried filling out some but not all text inputs and trying to submit the form to ensure the validation for input is still present
3. Typed in random/irregular characters into the text input fields to test how this would appear in the resulting Mad Lib
- This could be something restricted by using the pattern attribute for inputs followed by defining what kind of characters are allowed. This could be a dilemma for user experience since some users may want to extra themselves in inputs in unconventional ways that could be relevant/humorous for them. At the same time, it may make general sense that all users are kept to a certain, understandable standard when creating their Mad Lib records
4. Typed in conventional text into inputs to confirm their appearance in the resulting Mad Lib created
5. Clicked the back button after ending up in the Results page to see what happens if I enter new text into the input fields and to see what happens when I submit this (by checking the Results page that it redirects to and the Library page)
	- This proves to be a bug in that it isn’t a purposely designed process for users to be able to create new Mad Libs through this method. These new entries do add up also into the Library page. This is a bug that may have to be left to future development due to time constraints

#### Results page
1. Checked to see that the card with the created mad lib generates correctly
	- A drawback is noticed here in regards to the method used for generating the records in that there can be some irregular spacing in parts of the script. This is due to how the zip method that generates the result Mad Lib is designed, trying to zip string items together while also attempting to give appropriate space between string items. This, in terms of future development, would need further work on this zip method or to design a new method on how Mad Libs are generated. A new method, however, would potentially require a reconstruction of the database and collections, something worth considering if a new method is designed
2. Checked to see that the ‘Create Another’ and ‘View All Mad Libz’ buttons redirect the user to the right locations
3. Checked to see that the Delete button and function works properly, by relocating the user to the Library page with the user feedback message ‘Mad Lib deleted’

#### Library page
1. Checked to see that all records displayed match what is being stored in the MongoDb database
2. Checked to see that the right usernames are associated with the right Mad Lib creations
3. Made sure that, as a user, that I can only see the ‘Edit’ and ‘Delete’ buttons on the records that I have created
4. Checked to see that the ‘Edit’ button redirects the user to the right location, as well as testing the ‘Delete’ button to ensure that it carries out its function correctly
5. Tried to access links to the Edit page, Update function and Delete function for user A as user B (via url links) to check that user B is redirected to the Home page with the message ‘Error: Sorry, invalid user’

#### Edit page
1. Checked that prefilled input fields match the database entry and what was presented before on the Library page
2. Did input validation steps again as I did for the Insert Words page
3. Tested the Edit Mad Lib button after making sure inputs were filled in to confirm that  

#### Logout Feature
1. Clicked on the Logout menu item in the navbar to test out its functionality and to see that the user is correctly redirected to the landing page for non-logged-in visitors/users
2. Test clicking the back button on the browser to see that I correctly stay logged out, unable to access the previous pages that are only accessible to logged in users
	- Encountered bug here where images on the landing page do not render properly and appear in fallback/alt versions. The developer wasn’t able to decipher this issue in the time scope of this project and would consider is a bug left to be resolved in future development

#### Browser other than Google Chrome
Conducted the same tests on Safari, Firefox and Microsoft Edge as stated above. Below are the bugs/deviations I encountered when applying these tests to these browser compared to Google Chrome:
- Firefox and Safari did not seem to run Flask user sessions as they are supposed to work (giving/restricting access to certain pages on the website based on what user and if they are logged in or not). This was clear when using the back and forward buttons in these browsers between pages for logged in and not logged in users. This related to the browsers providing notices that the website was not secure. Unclear at this stage how to resolve this bug and will have to be resolved in future development due to time constraints of this project

- Smooth scrolling not working on Safari as a style in the CSS file. This is a known bug which is relatively minor in the case of this project, where only the ‘Learn More’ button (on the landing page for non-logged in visitors/user) looks to utilize this style, therefore not compromising the user experience of the website too extensively

### Testing for Mobile and Tablet devices
The same tests were done for smaller devices as were done for desktop (where these tests are described in greater detail. The only extra tests made included focusing on how the scrolling works, and how the pages/content rendered in smaller screen sizes. The only bug identified was related to the footer, where, for some but not all mobile devices, caused user experience issues when engaging with text inputs. The footer, as soon as the user scrolled down the page to the footer, the footer would become sticky, therefore blocking other content on the page. More significantly, as soon as the user wished to start typing into a text input (where there touchscreen keyboard would pop up), the footer would drag itself up to cover over all content below the text input the user was currently engaged with. A snapshot below can describe the issue better:
(insert mobile image)

- This could potentially be fixed by using a media query in CSS, adjusting the minimum height of the form container so it can push the footer away from view when the user is trying to type into the text inputs. This min-height style would need to be defined in pixels in order to not disturb the height set for the page container (being min-height 100vh, height 100%)

### Further Testing
- Asked friends, family and fellow classmates to review the website
	- Footer issue for mobile was mentioned here too by a family member
	- Suggestion to add security to usernames/passwords by setting maxlength attributes to the text input fields
	- General grammar/spelling corrections suggested for the Mad Lib templates and the landing page for non-logged-in users/visitors
- Did a review session with a Code Institute tutor Yoni Lavi to get further and extensive feedback on the near-to-final product, gaining the following feedback:
	- The information section in the landing page for non-logged in users needs to elaborate further as to what the website is before describing how it works
	- Buttons in the information section of the landing page could be placed closer together
	- Content of footer could be centered a bit more to give greater breathing room from the sides of the page. The Social Media header could either be removed or the header/text made smaller
	- It could be more intuitive to directly log in after signing up as opposed to being redirected to the Log In page
	- Look to describe in the README file the motivation behind using the two separate landing pages, one for logged in users and one for everyone else (bot logged in)
	- Recommendation text in the Create page could be highlighted even more to make this clearer/easier to read for users
	- For the Theme selection dropdown, specify even more clearly on the disabled option to ask the user to ‘Please choose a Mad Lib Theme’
	- Consider implementing greater consistency in the colour scheme of elements throughout the website to avoid too many styles being used
	- Try to get the buttons to be the same size regardless of the length of text inside each one
	- In the Library page, card displaying Mad Lib records could be aligned better to make it clearer for the user as to where they should start reading from
	- In Python code, try to use Guard Clauses in functions to avoid coding unnecessary ‘else’ statements, helping to reduce function sizes both horizontally and vertically
	- Use doc strings for comments in Python code so these can be more easily pulled to create description documentation of Python code (especially helpful for larger projects)

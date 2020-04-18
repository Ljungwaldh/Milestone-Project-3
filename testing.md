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

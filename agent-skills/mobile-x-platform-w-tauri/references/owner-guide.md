# Owner's guide template

Write this into the project's `context-v/docs/` (for example `Mobile-App-Guide-iPhone-And-Android.md`) with the project's own frontmatter conventions, and fill every `<…>` from the project facts in `SKILL.md`. Write for someone who isn't a developer: plain words, one visible result per step, and the agent doing the commands.

---

# Mobile App Guide: iPhone and Android

## What you're building

The <App> app on a phone is **a thin native shell that opens `<live URL>`** full screen, with its own icon, built with Tauri 2. The pages, sign-in and data are the same website, so **almost every change to <App> reaches the app instantly, with no new app release.** You only rebuild when the shell itself changes: its name, icon or version, or a yearly requirement from Apple or Google.

## How to use this guide with an agent

Open your coding agent in the repo and say which part you're on: *"I'm on Part 2, step 3 of the mobile app guide. Walk me through it."* The agent explains each step, runs the commands, and checks each one worked. Your job is the parts only a person can do: buying the developer accounts, clicking through Apple's and Google's websites, holding the phone, and saying "yes, upload it."

## Part 1: One-time setup

1. **Things you need:** a Mac (iPhone apps can only be built on one), about 60 GB free disk space, an iPhone and an Android phone with cables, and a password manager.
2. **Developer accounts:** Apple Developer Program (<price, enrollment choice: person or company>), Google Play Console (<price, the 12-testers-for-14-days rule if personal>). Write down the Apple Team ID.
3. **Install the tools** with the agent: Xcode, Node and <package manager>, Rust and its phone targets, CocoaPods, Android Studio with SDK and NDK. **Done when** every check passes.

## Part 2: Building the app the first time

Each step ends with something you can see. Don't move on until you've seen it.

1. **Choose the app's permanent ID** (`<identifier>`). It can never change once a store has it.
2. **Create the shell** in `<folder>/`, opening `<live URL>`. *You'll see:* the site in a desktop window.
3. **App icon** from one 1024×1024 square image. *You'll see:* the icon on the window.
4. **iPhone simulator.** *You'll see:* <App> on a pretend iPhone.
5. **Your real iPhone:** plug in, trust the Mac, turn on Developer Mode. *You'll see:* the icon on your home screen.
6. **Small fixes to the website for phones** (notch, keyboard, outside links). *You'll see:* Part 3's checklist passing.
7. **Android:** emulator, then a real phone with USB debugging on. *You'll see:* <App> on an Android home screen.
8. **Save it:** the agent commits the work and writes a changelog entry.

## Part 3: Testing on a phone

Test every new build on a real phone before sending it to anyone, using the agent's device checklist. **Anything that saves gets tried on `<test URL>`, never on <protected production data>.**

## Part 4: Getting it to people

- **iPhone, TestFlight:** create the app in App Store Connect; the agent builds the file and asks before uploading; upload with Transporter; add testers by email. **Builds expire after 90 days.**
- **Android, closed testing:** create the app in Play Console; save the upload key and its passwords in your password manager immediately; upload; add testers by email.
- **Public stores (later):** screenshots, description, privacy policy and support URLs. Apple's full review is where a website-in-a-shell is most likely to be turned down.

## Part 5: Keeping it working

- **No new release needed:** any change to the website.
- **New release needed:** name, icon, anything in `<folder>/`, Tauri security updates, TestFlight's 90 days, Apple's and Google's yearly requirements. Each release: raise the version, build both, test on a phone, then upload.

| When | What | Who |
|---|---|---|
| Every ~80 days | Fresh TestFlight build | <owner> with the agent |
| Every spring | Apple's newest-Xcode requirement: update and rebuild | <owner> with the agent |
| Every August | Google's target-API requirement: update and rebuild | <owner> with the agent |
| Yearly | Renew the Apple Developer Program | <owner> |
| Every few months | Check for Tauri updates | <owner> with the agent |

| Thing | Where | Never |
|---|---|---|
| Apple ID, App Store Connect, Play Console logins | Password manager | In the repo |
| Apple Team ID | Fine in the repo | — |
| Android upload key and its two passwords | Password manager, plus a backup | In the repo, chat or email |

## Risks to know about

- Apple may reject a website-in-a-shell from the public App Store (guideline 4.2).
- The app needs a connection.
- Emailed links open in the browser until universal links are set up.
- No push notifications yet.

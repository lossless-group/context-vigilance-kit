---
name: mobile-x-platform-w-tauri
description: "Helps a non-developer owner wrap a hosted web app in a Tauri 2 shell for iPhone and Android (and optionally Mac and Windows), then build, test on a real phone, deliver through TestFlight and Google Play, and maintain it, with the agent doing the technical work and teaching each step in plain words. Use when the user mentions a mobile app, iPhone, iOS, Android, Tauri, wrapping a website as an app, TestFlight, the App Store, Google Play, Play Console, Xcode, Android Studio, an app icon, or an app release or version bump, or is following an owner's guide in context-v/docs/. Covers choosing shell vs bundled app, the commands, a device test checklist, a release checklist, signing-key safety, and never uploading without the owner's explicit yes."
---

# Mobile Cross-Platform with Tauri (teach while you build)

The person you're helping is often **the app's owner, not a developer**: a founder, a commissioner, a client. Your job is to do the technical work and make every step understandable, so they can deliver and maintain the app themselves with an agent's help.

This skill covers the simplest shape that works: **a Tauri 2 shell that opens a live, hosted website full screen, with its own icon.** It suits a server-rendered app (Astro SSR, Rails, Django, Next with a server) that has no JSON API yet. Most website changes then reach the app with no new release.

## Contents

- Before you start: project facts
- Shell or something else?
- How to work with the owner
- Rules (never break these)
- The shape and the key settings
- Commands
- Testing ladder and device checklist
- Release checklist
- When to rebuild
- Common problems
- Limits of a shell
- `references/owner-guide.md`: the guide to write for the owner

## Before you start: project facts

Find these in the project's `context-v/` (a guide in `docs/`, a decision, `AGENTS.md`) before doing anything. Ask for any that are missing, and write them down where the next session will find them:

| Fact | Example | Why it matters |
|---|---|---|
| Live URL the app opens | `https://app.example.com` | The shell's `frontendDist` |
| Test URL (a staging or preview deployment) | `https://staging.example.com` | Everything that saves data is tested here |
| App identifier (reverse domain) | `com.example.app` | **Permanent** once a store has it |
| App name | `Example` | Home-screen label |
| Owner, and who holds the Apple and Google accounts | a person or a company | Who says yes to uploads, and whose name is on the store listing |
| Protected production data | "the live league", "customer accounts" | What a test must never change |
| The project's UI rules | a design-system skill, `DESIGN.md` | Website fixes for phones follow them |

If the project has no owner's guide yet, write one into `context-v/docs/` from `references/owner-guide.md`, filled with these facts. The guide is what the owner follows; this skill is what you follow while helping.

## Shell or something else?

Settle this once, and record it as a decision or exploration in `context-v/`:

- **Tauri shell around the live site** (this skill): days of work; every site change ships instantly. Weak offline; Apple may reject it from the *public* App Store as "minimum functionality" (guideline 4.2), though TestFlight's beta review is usually lighter.
- **Bundled Tauri app on an API:** a real app (instant screens, cache, native notifications), but the backend needs a JSON API and token sign-in first. The shell is a good first step towards it: it lives in its own folder and can later swap the URL for a bundled frontend.
- **Progressive Web App (PWA):** no store at all; web push on iOS needs the app installed to the home screen.
- **Capacitor:** more mature for mobile push; a second wrapper technology to learn.

## How to work with the owner

- **Find their place first.** Ask which part of the guide they're on, or read the guide and the app folder to work it out.
- **One step at a time.** Say what the step is for in one plain sentence, do it, then show the visible result ("you should now see…"). Don't chain steps silently.
- **Plain words.** Say "the iPhone project", not "the Xcode workspace in `gen/apple`", unless they ask. Define a term the first time ("a simulator is a pretend iPhone on your screen").
- **Exact clicks for anything they must do themselves** (Apple and Google websites, Xcode prompts, phone settings): the menu, the button, and what they'll see after.
- **When something fails,** say what it means in one sentence, fix it, and say whether it's likely to come back.
- **End each session** by saying where they are in the guide and what's next.

## Rules (never break these)

1. **Never upload to TestFlight, App Store Connect or Google Play, and never submit for review, without the owner saying yes to that specific build in this conversation.** Show the version number and what changed first.
2. **Never commit or paste signing secrets:** Android keystores (`*.jks`, `*.keystore`), `keystore.properties`, App Store Connect API keys (`*.p8`), or any password. Check `git status` before every commit in the app folder. Tell the owner to put each secret in a password manager the moment it's created.
3. **Never test writes against production.** Anything that saves is tried on the test URL; a test build points the shell there (see Commands). Follow the project's own production rules in full.
4. **The app identifier is permanent** once a store has it. Confirm it with the owner before the first build; never change it after the first upload.
5. **Raise the version** in `tauri.conf.json` for every store upload; both stores refuse a repeat.
6. **Fix phone problems in the website first,** following the project's UI rules. Those fixes help phone browsers too.
7. **Keep the Rust thin.** Every bit of native code is something the owner must maintain. Add a plugin or Rust code only when the website can't do the job, and explain why to the owner first.

## The shape and the key settings

```
mobile/                       # or another folder name the project prefers
  package.json                # @tauri-apps/cli as a dev dependency
  src-tauri/
    tauri.conf.json           # name, version, identifier, the URL it opens, icons, Apple team
    Cargo.toml, src/lib.rs    # the thin Rust shell
    icons/                    # generated by `tauri icon`
    gen/apple/                # iPhone project (committed)
    gen/android/              # Android project (committed; keystore.properties is NOT)
```

Keep it in its own folder beside the web app, not inside it, so the web app's build and deploy are untouched.

In `tauri.conf.json`:

- `"identifier": "<reverse domain>"`
- `"build": { "frontendDist": "<live URL>" }`: a remote URL, so nothing is bundled and the app loads the live site
- `"bundle": { "iOS": { "developmentTeam": "<Apple Team ID>" } }`

A pure shell needs no Tauri commands or IPC. If a page on the remote site ever needs a plugin, it must be allowed for that origin through a capability with `remote.urls`. That's a deliberate security decision, not a quick fix.

## Commands

Run from the shell's folder, with the project's package manager (pnpm shown). Explain what each does when you run it.

| Purpose | Command |
|---|---|
| Add Tauri to the folder | `pnpm add -D @tauri-apps/cli@latest`, then `pnpm tauri init` |
| Desktop window (quick check) | `pnpm tauri dev` |
| Generate icons | `pnpm tauri icon <path-to-1024px.png>` (square, no transparency for iOS) |
| iPhone: first-time project | `pnpm tauri ios init` |
| iPhone: simulator or plugged-in phone | `pnpm tauri ios dev` (choose the device; `--open` opens Xcode) |
| iPhone: store build | `pnpm tauri ios build --export-method app-store-connect` |
| Android: first-time project | `pnpm tauri android init` |
| Android: emulator or plugged-in phone | `pnpm tauri android dev` |
| Android: store build | `pnpm tauri android build --aab` |
| Test build against the test URL | add `--config '{"build":{"frontendDist":"<test URL>"}}'` to a dev or build command |
| Check for updates | `pnpm outdated` in the folder, and `cargo update --dry-run` in `src-tauri/` |

Setup checks: `xcode-select -p`; `rustup target list --installed` (iOS: `aarch64-apple-ios`, `aarch64-apple-ios-sim`, `x86_64-apple-ios`; Android: `aarch64-linux-android`, `armv7-linux-androideabi`, `i686-linux-android`, `x86_64-linux-android`); `pod --version`; and `JAVA_HOME`, `ANDROID_HOME` and `NDK_HOME` set in the owner's shell profile (Android Studio's bundled JBR for Java). **Follow [Tauri's prerequisites page](https://v2.tauri.app/start/prerequisites/) for current versions, not memory.**

Uploading: the `.ipa` through Apple's **Transporter** app (simplest for an owner) or `xcrun altool`; the `.aab` through Play Console's web upload. Android signing follows [Tauri's Google Play guide](https://v2.tauri.app/distribute/google-play/): a keystore made with `keytool`, `gen/android/keystore.properties` (gitignored), and the signing block in `gen/android/app/build.gradle.kts`. iOS follows [Tauri's App Store guide](https://v2.tauri.app/distribute/app-store/).

## Testing ladder and device checklist

Go up one rung at a time; each must pass before the next.

1. **Desktop window** (`tauri dev`): the shell opens the site.
2. **Simulator / emulator:** layout, sign-in, navigation.
3. **The owner's own phone over USB:** the full device checklist.
4. **TestFlight internal / Play internal testing:** the owner installs the store build itself, the exact file users will get.
5. **Real users** (TestFlight external testers, Play closed testing), only with the owner's yes.

Device checklist (copy into your reply and tick with the owner as they try each one):

- [ ] Signs in; **still signed in after a force-quit and reopen.** A session cookie with no expiry is dropped when the app closes, so check the site's cookie settings if not.
- [ ] Nothing under the notch, camera cut-out or home bar, portrait and landscape (`viewport-fit=cover` in the viewport meta plus `env(safe-area-inset-*)` padding, if needed)
- [ ] Every page has a way back without a browser back button
- [ ] Forms aren't covered by the keyboard; tapping an input doesn't zoom the page (inputs at 16px or more)
- [ ] Outside links open in the system browser and the owner can return. Known Tauri issue: on mobile, links opened through the shell plugin can land in an in-app view with no way back ([plugins-workspace #3401](https://github.com/tauri-apps/plugins-workspace/issues/3401)); test on a real device
- [ ] Emailed links (password reset, invites) work; they open in the browser, not the app, until universal links or app links are set up
- [ ] Anything that refreshes on a timer resumes after the app is backgrounded
- [ ] Every colour mode the site has
- [ ] Airplane mode shows something sensible and recovers
- [ ] Icon, name and launch look right on the home screen

## Release checklist

1. Version raised in `tauri.conf.json`.
2. Both apps built; the device checklist passed on the store build.
3. The owner shown the version and what changed, and says yes.
4. Upload. For TestFlight, note the date: **builds expire after 90 days.**
5. Commit the app folder's changes (never the secrets) and write a changelog entry if the project keeps one.

## When to rebuild

Tell the owner this when they ask "do I need a new app?"

- **No:** any change to the website. It's live in the app the next time someone opens it.
- **Yes:**
  - the name, icon, launch screen, or anything in the app folder;
  - Tauri security updates;
  - TestFlight's 90-day expiry (upload fresh at least every ~80 days);
  - Apple's yearly minimum Xcode/SDK for uploads (usually announced each spring);
  - Google's yearly minimum target Android API level (usually each August).

Put those dates in the owner's guide as a calendar.

## Common problems

| What the owner sees | What it means | Fix |
|---|---|---|
| "No development team" / signing error | The Apple Team ID isn't set | Set `bundle.iOS.developmentTeam`, or pick the team in Xcode's Signing tab |
| iPhone says "Untrusted Developer" | First install from this Mac | Settings → General → VPN & Device Management → trust |
| iPhone won't install at all | Developer Mode is off | Settings → Privacy & Security → Developer Mode, then restart |
| `xcrun: error` or `xcode-select` errors | Command-line tools point at the wrong place | `sudo xcode-select -s /Applications/Xcode.app` |
| Android "NDK not found" / `ANDROID_HOME` errors | Shell settings missing | Add the three variables to the shell profile and open a new terminal |
| Blank white screen | No network, or the URL in `frontendDist` is wrong | Check the connection and the config |
| Store rejects the upload as a duplicate | Version not raised | Raise it and rebuild |
| TestFlight app won't open for testers | The build expired (90 days) | Upload a fresh build |

## Limits of a shell

Say these plainly when the owner asks for more:

- **No offline:** the app is the website.
- **No push notifications** without native work; on Tauri mobile, remote push needs a plugin or native code. Spike it on a real phone before promising it.
- **Public App Store risk** under guideline 4.2 until the app does something a website can't.
- Push, offline and a faster native feel come from the **bundled app on an API**. If the project hasn't explored that yet, suggest writing an exploration in `context-v/explorations/` rather than bolting native features onto the shell.

## Store accounts (for the owner's guide)

- **Apple Developer Program:** $99 a year. Enrolling as an organization needs a free D-U-N-S number and takes longer, but shows the company as the maker; an individual enrollment is faster but can't simply be moved to a company later.
- **Google Play Console:** $25 once. A **personal** account created after 2023-11-13 must run a closed test with **at least 12 testers opted in for 14 days in a row** before publishing to production ([Google's rule](https://support.google.com/googleplay/android-developer/answer/14151465)). Organization accounts skip it but need a D-U-N-S number.
- Check both for current prices and rules before quoting them; they change.

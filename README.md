# hamster-kombat-auto-upgrade
Utilizes hamster kombat's internal api to auto upgrade any available mining asset.


# Usage
You will need your bearer token for that, here are the steps for it:
1. Get [HTTP-ToolKit](https://httptoolkit.com/)
2. Get an Emulator like [Bluestacks 5](https://www.bluestacks.com/) and root it. (For bluestacks 5 use [this guide](https://kimlisoft.com/how-to-root-bluestacks-5/))
3. Make sure you have [python](https://www.python.org/downloads/) downloaded.
4. Download telegram and login over there on the emulator's instance.
5. Install all depends from `requirements.txt` with `python -m pip install -r requirements.txt`
6. Launch bluestacks 5 and go to the `menu > settings` and click on `Advanced` tab. You will see something like [this](https://raw.githubusercontent.com/fw-real/hamster-kombat-auto-upgrade/main/screenshots/adbss.png) if ADB is enabled, if not, enable it and get the IP:PORT from there.
7. Download [HTTP-Toolkit-Android](https://play.google.com/store/apps/details?id=tech.httptoolkit.android.v1&hl=en_IN) there.
8. Open a terminal to the `adb_files` folder and run `adb connect ip:port`.
9. Launch HTTP-Toolkit and scroll till you find the `Android via ADB` tab like in [this screenshot](https://raw.githubusercontent.com/fw-real/hamster-kombat-auto-upgrade/main/screenshots/httptoolkitss.png), click on it and then click on the blue option which contains the `ip:port`.
10. Go to view tab after that and you should be getting intercepted, for detailed documentation visit the [official guide on intercepting android with http-toolkit](https://httptoolkit.com/docs/guides/android/)
11. Once your interception is setup, you should see [this](https://raw.githubusercontent.com/fw-real/hamster-kombat-auto-upgrade/main/screenshots/interceptingss.png) when HTTP-Toolkit android is opened (it will usualy open itself but if it didn't just open and check) where both user and system trust are enabled, if everything went correct.
12. Launch telegram and then open hamster kombat game while you are being intercepted.
13. After you have successfully opened hamster kombat and you are in the game, go back to HTTP-Toolkit PC and press `ctrl+f` or search for `https://api.hamsterkombat.io/auth/me-telegram`. Once you find it, click on it and see the headers, one of them would be `Authorization`: `Bearer tokenhere` copy the part after the `Bearer` thats your authorization token, you are now done with intercepting, you can close everything as per your liking. Here's a [screenshot](https://raw.githubusercontent.com/fw-real/hamster-kombat-auto-upgrade/main/screenshots/req.png) so you get what I mean better on how to get the token.
14. Now run `python main.py` and paste the token.
15. If token was valid, you can now use the tool.
16. Use the first option to fetch available upgrades for your account and see which one you want to spam upgrade. Note down the `ID` of the upgrade once you choose.
17. Use the second option to spam upgrade, enter the id for the upgrade you got from the first option and press enter, then enter the amount of times you want to upgrade it. (Keep in mind that you should have the sufficient balance and have entered a valid upgrade id to successfully upgrade).
18. If successfull inputs are passed, the asset will start upgrade as per your inputs.


# Issue/PR
if you got a bug or suggestion or update or something, open an issue/pr respectively. or hit me up on discord at `@nostorian`.

# License
This project is licensed under GNU General Public License v3.0

from obp_oauth2_flow import ObpOAuth2Flow


bank = "demo.co.uk"
url = "https://set-your-hola-domain.here"
iban = "DE1234567891234"
username = "username"
password = "password"
show_accounts_test = ObpOAuth2Flow()


try:
    show_accounts_test.setup_method_firefox()
    show_accounts_test.show_accountsBG(
        url,
        bank,
        iban=iban,
        username=username,
        password=password,
        # This is the default, actually.
        # The mail script will then return "123", which obp api will accept when
        # 'suggested_default_sca_method=DUMMY' is set
        # If you use a real mail host, you also have to set mail user and password
        mail_host="DUMMY",
        # The default, will not set permissions for getting balances and transactions and check for correct errors
        # For getting balances and transactions, set to false
        accounts_only=True
    )
    print("Worked!")
except Exception as e:
    print("Failed: " + str(e))

finally:
    show_accounts_test.teardown_method()
print("done")


from manufactorum import app


if __name__ == '__main__':
    print("Don't use this script to run your server in production! "
          "Debug mode is enabled!")
    app.run(debug=True)

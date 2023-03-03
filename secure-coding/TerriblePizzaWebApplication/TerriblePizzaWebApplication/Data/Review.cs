using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.Data.Sqlite;

namespace TerriblePizzaWebApplication.Data {
    public class Review {
        public DateTime CreationDate { get; set; }
        public string ReviewText { get; set; }
        public UserAccount User { get; set; }

        public Review(DateTime created, string review, UserAccount user) {
            CreationDate = created;
            ReviewText = review;
            User = user;
        }

        public Review() 
        {
        }
    }
}

using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace TerriblePizzaWebApplication.Data {
    public class MyDbContext : DbContext{
        public MyDbContext(DbContextOptions<MyDbContext> options)
                   : base(options) {
        }

        public DbSet<UserAccount> Account { get; set; }
        public DbSet<Pizza> MyPizza { get; set; }


        protected override void OnModelCreating(ModelBuilder modelBuilder) {
            modelBuilder.Entity<UserAccount>().HasData(GetAccounts());
            base.OnModelCreating(modelBuilder);
        }

        private List<UserAccount> GetAccounts() {
            return new List<UserAccount>();
        }
    }
}

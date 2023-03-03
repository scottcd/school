using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace TerriblePizzaWebApplication.Data {
    public class MyDbService {
        private MyDbContext dbContext;
        public MyDbService(MyDbContext dbContext) {
            this.dbContext = dbContext;
        }
        
        public async Task<List<UserAccount>> GetAllAccountsAsync() {
            
            return await dbContext.Account.FromSqlRaw("Select * FROM Account").ToListAsync();
        }
        
        public async Task<List<Pizza>> GetAllPizzasAsync() {

            return await dbContext.MyPizza.FromSqlRaw("Select * FROM Pizza").ToListAsync();
        }

        public async Task<UserAccount> GetAccountLoginAsync(string username, string password) {

            return await dbContext.Account.FromSqlRaw($"Select * FROM Account Where username='{username}' AND password='{password}'").FirstOrDefaultAsync();
        }
        public async Task<UserAccount> GetAccountIdAsync(int id) {

            return await dbContext.Account.FromSqlRaw($"Select * FROM Account Where id='{id}'").FirstOrDefaultAsync();
        }
        public async Task<UserAccount> AddAccountAsync(UserAccount person) {
            try {
                dbContext.Account.Add(person);
                await dbContext.SaveChangesAsync();
            }
            catch (Exception e) {
                System.Diagnostics.Debug.WriteLine($"\n\n\n{e.StackTrace}\n\n {e.Message}\n\n\n");
                return null;
            }
            return person;
        }

        public async Task<UserAccount> UpdateAccountAsync(UserAccount account) {
            try {
                var foundAccount = dbContext.Account.FirstOrDefault(p => p.Id == account.Id);
                if (foundAccount != null) {
                    foundAccount.TotalPizzas = account.TotalPizzas;
                    foundAccount.TotalMoney = account.TotalMoney;
                    dbContext.Account.Update(foundAccount);
                    await dbContext.SaveChangesAsync();
                }
            }
            catch (Exception) {
                throw;
            }
            return account;
        }
        public async Task DeleteAccountAsync(UserAccount account) {
            try {
                dbContext.Account.Remove(account);
                await dbContext.SaveChangesAsync();
            }
            catch (Exception) {
                throw;
            }
        }
    }
}
